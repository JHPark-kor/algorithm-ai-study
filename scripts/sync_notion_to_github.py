#!/usr/bin/env python3
"""
Sync Notion paper-review cards into the study GitHub repository.

What it does:
- reads Notion page text and attached PDF files
- downloads PDF files into algorithms/{algorithm}/02_paper_review/papers/
- asks the OpenAI API to write a paper-abstract-style summary
- updates algorithms/{algorithm}/02_paper_review/README.md inside a managed section

Required environment variables:
- NOTION_API_KEY
- OPENAI_API_KEY

Typical usage:
python scripts/sync_notion_to_github.py \
  --algorithm svm \
  --week w7 \
  --notion-pages "https://app.notion.com/p/w7_svm_PaperReview-..."
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


NOTION_API_BASE = "https://api.notion.com/v1"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
DEFAULT_NOTION_VERSION = "2026-03-11"
DEFAULT_OPENAI_MODEL = "gpt-5.6-terra"


@dataclass
class NotionFile:
    name: str
    url: str
    source: str


@dataclass
class ReviewRecord:
    page_id: str
    page_title: str
    notion_url: str
    author: str
    text: str
    files: list[NotionFile] = field(default_factory=list)
    downloaded_pdfs: list[Path] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)


def normalize_uuid(raw: str) -> str:
    compact = re.sub(r"[^0-9a-fA-F]", "", raw)
    if len(compact) != 32:
        raise ValueError(f"Notion page id must contain 32 hex characters: {raw}")
    return (
        f"{compact[0:8]}-{compact[8:12]}-{compact[12:16]}-"
        f"{compact[16:20]}-{compact[20:32]}"
    ).lower()


def notion_id_from_url_or_id(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("empty Notion page id/url")

    parsed = urllib.parse.urlparse(value)
    query = urllib.parse.parse_qs(parsed.query)
    if query.get("p"):
        return normalize_uuid(query["p"][0])

    matches = re.findall(r"[0-9a-fA-F]{32}", value.replace("-", ""))
    if not matches:
        raise ValueError(f"Could not find a Notion id in: {value}")
    return normalize_uuid(matches[-1])


def split_sources(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in re.split(r"[,\n]+", value) if part.strip()]


def safe_filename(value: str, fallback: str = "untitled") -> str:
    value = value.strip() or fallback
    value = re.sub(r"[\\/:*?\"<>|]+", " ", value)
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"_+", "_", value)
    value = value.strip("._- ")
    return value[:120] or fallback


def plain_text(items: list[dict[str, Any]] | None) -> str:
    if not items:
        return ""
    return "".join(item.get("plain_text", "") for item in items)


def property_to_text(prop: dict[str, Any]) -> str:
    kind = prop.get("type")
    if kind == "title":
        return plain_text(prop.get("title"))
    if kind == "rich_text":
        return plain_text(prop.get("rich_text"))
    if kind == "status":
        return (prop.get("status") or {}).get("name", "")
    if kind == "select":
        return (prop.get("select") or {}).get("name", "")
    if kind == "multi_select":
        return ", ".join(item.get("name", "") for item in prop.get("multi_select", []))
    if kind == "people":
        return ", ".join(person.get("name", "") for person in prop.get("people", []))
    if kind == "url":
        return prop.get("url") or ""
    if kind == "files":
        return ", ".join(item.get("name", "") for item in prop.get("files", []))
    if kind == "checkbox":
        return "true" if prop.get("checkbox") else "false"
    if kind == "date":
        date = prop.get("date") or {}
        return date.get("start", "")
    if kind == "number":
        number = prop.get("number")
        return "" if number is None else str(number)
    return ""


def page_title(page: dict[str, Any]) -> str:
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            title = property_to_text(prop)
            if title:
                return title
    return "Untitled"


def page_author(page: dict[str, Any]) -> str:
    preferred = ["담당자", "작성자", "발표자", "Author", "Assignee", "Owner"]
    props = page.get("properties", {})
    for name in preferred:
        if name in props:
            value = property_to_text(props[name])
            if value:
                return value
    for prop in props.values():
        if prop.get("type") == "people":
            value = property_to_text(prop)
            if value:
                return value
    return "unknown"


def page_url(page: dict[str, Any], page_id: str) -> str:
    return page.get("url") or f"https://www.notion.so/{page_id.replace('-', '')}"


class NotionClient:
    def __init__(self, token: str, version: str = DEFAULT_NOTION_VERSION) -> None:
        self.token = token
        self.version = version

    def request(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{NOTION_API_BASE}{path}"
        data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self.version,
            "Content-Type": "application/json",
        }
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=45) as res:
                return json.loads(res.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Notion API error {exc.code}: {detail}") from exc

    def retrieve_page(self, page_id: str) -> dict[str, Any]:
        return self.request("GET", f"/pages/{page_id}")

    def retrieve_block_children(self, block_id: str) -> list[dict[str, Any]]:
        children: list[dict[str, Any]] = []
        cursor: str | None = None
        while True:
            query = {"page_size": "100"}
            if cursor:
                query["start_cursor"] = cursor
            path = f"/blocks/{block_id}/children?{urllib.parse.urlencode(query)}"
            data = self.request("GET", path)
            children.extend(data.get("results", []))
            if not data.get("has_more"):
                return children
            cursor = data.get("next_cursor")
            time.sleep(0.35)

    def query_source(self, source_id: str, source_kind: str) -> list[dict[str, Any]]:
        pages: list[dict[str, Any]] = []
        cursor: str | None = None
        endpoint = "data_sources" if source_kind == "data_source" else "databases"
        source_uuid = notion_id_from_url_or_id(source_id)
        while True:
            body: dict[str, Any] = {"page_size": 100}
            if cursor:
                body["start_cursor"] = cursor
            data = self.request("POST", f"/{endpoint}/{source_uuid}/query", body)
            pages.extend(data.get("results", []))
            if not data.get("has_more"):
                return pages
            cursor = data.get("next_cursor")
            time.sleep(0.35)


def block_rich_text(block: dict[str, Any]) -> str:
    kind = block.get("type")
    data = block.get(kind, {}) if kind else {}
    if isinstance(data, dict):
        if "rich_text" in data:
            return plain_text(data.get("rich_text"))
        if "text" in data:
            return plain_text(data.get("text"))
        if "expression" in data:
            return data.get("expression", "")
    if kind == "child_page":
        return data.get("title", "")
    if kind == "child_database":
        return data.get("title", "")
    return ""


def block_to_markdown_line(block: dict[str, Any]) -> str:
    kind = block.get("type")
    text = block_rich_text(block).strip()
    if not text:
        return ""
    if kind and kind.startswith("heading_"):
        level = {"heading_1": "#", "heading_2": "##", "heading_3": "###", "heading_4": "####"}.get(kind, "###")
        return f"\n{level} {text}\n"
    if kind == "bulleted_list_item":
        return f"- {text}"
    if kind == "numbered_list_item":
        return f"1. {text}"
    if kind == "quote":
        return f"> {text}"
    if kind == "to_do":
        checked = block.get("to_do", {}).get("checked", False)
        return f"- [{'x' if checked else ' '}] {text}"
    if kind == "equation":
        return f"`{text}`"
    if kind == "table_row":
        cells = block.get("table_row", {}).get("cells", [])
        return " | ".join(plain_text(cell).strip() for cell in cells)
    return text


def file_from_notion_obj(obj: dict[str, Any], source: str) -> NotionFile | None:
    file_type = obj.get("type")
    url = ""
    if file_type == "file":
        url = (obj.get("file") or {}).get("url", "")
    elif file_type == "external":
        url = (obj.get("external") or {}).get("url", "")
    elif file_type == "file_upload":
        return None

    name = obj.get("name") or Path(urllib.parse.urlparse(url).path).name or "notion_file"
    if not url:
        return None
    return NotionFile(name=name, url=url, source=source)


def page_property_files(page: dict[str, Any]) -> list[NotionFile]:
    files: list[NotionFile] = []
    for prop_name, prop in page.get("properties", {}).items():
        if prop.get("type") != "files":
            continue
        for item in prop.get("files", []):
            notion_file = file_from_notion_obj(item, f"property:{prop_name}")
            if notion_file:
                files.append(notion_file)
    return files


def block_file(block: dict[str, Any]) -> NotionFile | None:
    kind = block.get("type")
    if kind not in {"file", "pdf"}:
        return None
    data = block.get(kind, {})
    if not isinstance(data, dict):
        return None
    notion_file = file_from_notion_obj(data, f"block:{kind}")
    if notion_file and kind == "pdf" and not notion_file.name.lower().endswith(".pdf"):
        notion_file.name = f"{notion_file.name}.pdf"
    return notion_file


def read_blocks_recursive(client: NotionClient, block_id: str, depth: int = 0) -> tuple[str, list[NotionFile]]:
    if depth > 8:
        return "", []

    lines: list[str] = []
    files: list[NotionFile] = []
    for block in client.retrieve_block_children(block_id):
        line = block_to_markdown_line(block)
        if line:
            lines.append(line)
        notion_file = block_file(block)
        if notion_file:
            files.append(notion_file)
        if block.get("has_children"):
            child_text, child_files = read_blocks_recursive(client, block["id"], depth + 1)
            if child_text:
                lines.append(child_text)
            files.extend(child_files)
    return "\n".join(lines), files


def filter_page(
    page: dict[str, Any],
    *,
    week: str,
    algorithm: str,
    status_prop: str,
    status_done: str,
    type_prop: str,
    type_value: str,
    week_prop: str,
    algorithm_prop: str,
) -> bool:
    props = page.get("properties", {})

    def prop_value(name: str) -> str:
        return property_to_text(props[name]).lower() if name in props else ""

    if status_prop in props and status_done:
        if status_done.lower() not in prop_value(status_prop):
            return False
    if type_prop in props and type_value:
        if type_value.lower() not in prop_value(type_prop):
            return False
    if week_prop in props and week:
        if week.lower() not in prop_value(week_prop):
            return False
    if algorithm_prop in props and algorithm:
        if algorithm.lower() not in prop_value(algorithm_prop):
            return False
    return True


def download_file(file: NotionFile, target_dir: Path, week: str, author: str, dry_run: bool = False) -> Path | None:
    parsed_name = urllib.parse.unquote(file.name)
    if not parsed_name.lower().endswith(".pdf") and ".pdf" not in urllib.parse.unquote(file.url).lower():
        return None

    if not parsed_name.lower().endswith(".pdf"):
        parsed_name = f"{parsed_name}.pdf"

    stem = safe_filename(Path(parsed_name).stem)
    author_part = safe_filename(author, "unknown")
    if not stem.lower().startswith(week.lower()):
        filename = f"{safe_filename(week)}_{stem}_{author_part}.pdf"
    else:
        filename = f"{stem}_{author_part}.pdf"

    path = target_dir / filename
    if dry_run:
        return path

    target_dir.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(file.url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as res:
        content = res.read()
    if path.exists() and path.read_bytes() == content:
        return path
    path.write_bytes(content)
    return path


def extract_pdf_text(pdf_path: Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return ""
    try:
        reader = PdfReader(str(pdf_path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        return ""


def openai_summary(prompt_template: str, record: ReviewRecord, model: str) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required to summarize reviews")

    source_text = record.text.strip()
    if len(source_text) < 300:
        pdf_texts = [extract_pdf_text(path) for path in record.downloaded_pdfs]
        source_text = "\n\n".join(text for text in pdf_texts if text.strip()) or source_text

    source_text = source_text[:45000]
    user_prompt = f"""{prompt_template}

메타데이터:
- Notion page title: {record.page_title}
- 작성자: {record.author}
- Notion URL: {record.notion_url}
- 첨부 PDF: {", ".join(path.name for path in record.downloaded_pdfs) or "없음"}

Notion 본문:
{source_text}
"""

    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "paper_source": {"type": "string"},
            "keywords": {"type": "array", "items": {"type": "string"}, "minItems": 3, "maxItems": 8},
            "overview": {"type": "string"},
            "data": {"type": "string"},
            "method": {"type": "string"},
            "result": {"type": "string"},
            "project_idea": {"type": "string"},
        },
        "required": ["paper_source", "keywords", "overview", "data", "method", "result", "project_idea"],
    }

    payload = {
        "model": model,
        "store": False,
        "input": [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": user_prompt}],
            }
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "paper_review_summary",
                "schema": schema,
                "strict": True,
            }
        },
        "max_output_tokens": 1800,
    }
    req = urllib.request.Request(
        OPENAI_RESPONSES_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            data = json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error {exc.code}: {detail}") from exc

    output_text = data.get("output_text")
    if not output_text:
        parts: list[str] = []
        for item in data.get("output", []):
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"}:
                    parts.append(content.get("text", ""))
        output_text = "\n".join(parts)

    if not output_text:
        raise RuntimeError("OpenAI response did not contain output text")
    return json.loads(output_text)


def markdown_link(path: Path, base_dir: Path) -> str:
    rel = path.relative_to(base_dir).as_posix()
    return f"[{path.name}]({rel})"


def build_markdown_section(records: list[ReviewRecord], algorithm: str, week: str, readme_dir: Path) -> str:
    title = f"## {week.upper()} {algorithm.upper()} 논문 리뷰 요약"
    lines = [
        title,
        "",
        "> 이 영역은 Notion 과제 내용을 바탕으로 자동 갱신됩니다. 자세한 원문은 Notion과 첨부 PDF를 확인합니다.",
        "",
    ]

    for record in records:
        summary = record.summary
        keywords = summary.get("keywords") or []
        pdf_links = ", ".join(markdown_link(path, readme_dir) for path in record.downloaded_pdfs) or "PDF 확인 필요"
        lines.extend(
            [
                f"### {record.author}",
                "",
                f"- 논문 출처: {summary.get('paper_source', '확인 필요')}",
                f"- 주요 키워드: {', '.join(keywords) if keywords else '확인 필요'}",
                f"- PDF: {pdf_links}",
                f"- Notion 원본: [원문 보기]({record.notion_url})",
                "",
                "#### 논문 개요",
                "",
                summary.get("overview", "확인 필요").strip(),
                "",
                "#### 데이터 및 방법",
                "",
                f"- 데이터: {summary.get('data', '확인 필요')}",
                f"- 방법론: {summary.get('method', '확인 필요')}",
                "",
                "#### 주요 결과 및 프로젝트 연결",
                "",
                f"- 주요 결과: {summary.get('result', '확인 필요')}",
                f"- 3주차 프로젝트 아이디어: {summary.get('project_idea', '확인 필요')}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def update_readme(readme_path: Path, section: str, week: str, category: str, dry_run: bool = False) -> None:
    start = f"<!-- notion-sync:{week}:{category}:start -->"
    end = f"<!-- notion-sync:{week}:{category}:end -->"
    managed = f"{start}\n{section}{end}\n"

    if readme_path.exists():
        original = readme_path.read_text(encoding="utf-8")
    else:
        original = "# Paper Review\n"

    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\n?", re.DOTALL)
    if pattern.search(original):
        updated = pattern.sub(managed, original)
    else:
        updated = original.rstrip() + "\n\n" + managed

    if not dry_run:
        readme_path.parent.mkdir(parents=True, exist_ok=True)
        readme_path.write_text(updated, encoding="utf-8")


def load_prompt() -> str:
    prompt_path = Path("prompts/paper_review_summary.txt")
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "논문 리뷰를 읽고 논문 개요 문체로 요약한다."


def collect_records(args: argparse.Namespace) -> list[ReviewRecord]:
    token = os.getenv("NOTION_API_KEY")
    if not token:
        raise RuntimeError("NOTION_API_KEY is required")

    client = NotionClient(token, os.getenv("NOTION_VERSION", DEFAULT_NOTION_VERSION))
    page_ids = [notion_id_from_url_or_id(item) for item in split_sources(args.notion_pages)]

    if args.notion_source_id:
        candidates = client.query_source(args.notion_source_id, args.notion_source_kind)
        for page in candidates:
            if filter_page(
                page,
                week=args.week,
                algorithm=args.algorithm,
                status_prop=args.status_prop,
                status_done=args.status_done,
                type_prop=args.type_prop,
                type_value=args.type_value,
                week_prop=args.week_prop,
                algorithm_prop=args.algorithm_prop,
            ):
                page_ids.append(page["id"])

    if not page_ids:
        raise RuntimeError("Provide --notion-pages or --notion-source-id")

    records: list[ReviewRecord] = []
    seen: set[str] = set()
    for page_id in page_ids:
        if page_id in seen:
            continue
        seen.add(page_id)
        page = client.retrieve_page(page_id)
        text, block_files = read_blocks_recursive(client, page_id)
        record = ReviewRecord(
            page_id=page_id,
            page_title=page_title(page),
            notion_url=page_url(page, page_id),
            author=page_author(page),
            text=text,
            files=page_property_files(page) + block_files,
        )
        records.append(record)
    return records


def run(args: argparse.Namespace) -> int:
    root = Path(args.repo_root).resolve()
    category = "paper_review"
    target_dir = root / "algorithms" / args.algorithm / "02_paper_review"
    papers_dir = target_dir / "papers"
    readme_path = target_dir / "README.md"
    prompt = load_prompt()

    records = collect_records(args)
    for record in records:
        for notion_file in record.files:
            downloaded = download_file(notion_file, papers_dir, args.week, record.author, args.dry_run)
            if downloaded:
                record.downloaded_pdfs.append(downloaded)

        record.summary = openai_summary(prompt, record, os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL))

    section = build_markdown_section(records, args.algorithm, args.week, readme_path.parent)
    update_readme(readme_path, section, args.week, category, args.dry_run)

    print(f"Processed {len(records)} Notion paper review page(s).")
    print(f"README: {readme_path}")
    for record in records:
        print(f"- {record.author}: {record.page_title}")
        for pdf in record.downloaded_pdfs:
            print(f"  PDF: {pdf}")

    if args.dry_run:
        print("\n--- README section preview ---")
        print(section)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync Notion paper-review pages to GitHub folders and README summaries.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:
              python scripts/sync_notion_to_github.py --algorithm svm --week w7 --notion-pages "URL1,URL2"

              NOTION_SOURCE_ID=... python scripts/sync_notion_to_github.py --algorithm svm --week w7
            """
        ),
    )
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--algorithm", default=os.getenv("STUDY_ALGORITHM", "svm"))
    parser.add_argument("--week", default=os.getenv("STUDY_WEEK", "w7"))
    parser.add_argument("--notion-pages", default=os.getenv("NOTION_PAGES", ""), help="Comma/newline-separated Notion page URLs or IDs.")
    parser.add_argument("--notion-source-id", default=os.getenv("NOTION_SOURCE_ID", ""), help="Optional Notion data source/database ID.")
    parser.add_argument("--notion-source-kind", default=os.getenv("NOTION_SOURCE_KIND", "data_source"), choices=["data_source", "database"])
    parser.add_argument("--status-prop", default=os.getenv("NOTION_STATUS_PROP", "상태"))
    parser.add_argument("--status-done", default=os.getenv("NOTION_STATUS_DONE", "완료"))
    parser.add_argument("--type-prop", default=os.getenv("NOTION_TYPE_PROP", "유형"))
    parser.add_argument("--type-value", default=os.getenv("NOTION_TYPE_VALUE", "논문"))
    parser.add_argument("--week-prop", default=os.getenv("NOTION_WEEK_PROP", "주차"))
    parser.add_argument("--algorithm-prop", default=os.getenv("NOTION_ALGORITHM_PROP", "알고리즘"))
    parser.add_argument("--dry-run", action="store_true", help="Read and summarize, but do not write files.")
    return parser.parse_args()


if __name__ == "__main__":
    try:
        raise SystemExit(run(parse_args()))
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
