#!/usr/bin/env python3
"""
Convert Hugo Academic publication pages to Quarto format.
Reads content/publication/*/index.md and writes publications/*/index.qmd
"""

import os
import re
import shutil
import tomllib
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SRC_DIR = REPO_ROOT / "content" / "publication"
DST_DIR = REPO_ROOT / "publications"

PUB_TYPE_MAP = {
    "0": "Uncategorized",
    "1": "Conference Paper",
    "2": "Journal Article",
    "3": "Manuscript",
    "4": "Report",
    "5": "Book",
    "6": "Book Section",
}


def strip_doi_prefix(doi: str) -> str:
    doi = doi.strip()
    for prefix in ["https://doi.org/", "http://doi.org/",
                   "https://dx.doi.org/", "http://dx.doi.org/"]:
        if doi.startswith(prefix):
            doi = doi[len(prefix):]
            break
    doi = doi.replace("%2F", "/").replace("%3A", ":").strip()
    return doi


def parse_yaml_fm(text: str) -> dict:
    """Parse YAML frontmatter using the yaml library."""
    try:
        return yaml.safe_load(text) or {}
    except yaml.YAMLError:
        return {}


def parse_toml_fm(text: str) -> dict:
    """Parse TOML frontmatter using tomllib."""
    try:
        return tomllib.loads(text)
    except Exception:
        return {}


def split_frontmatter(content: str):
    content = content.strip()
    if content.startswith("+++"):
        end = content.find("+++", 3)
        if end == -1:
            return content, "", "toml"
        return content[3:end].strip(), content[end + 3:].strip(), "toml"
    elif content.startswith("---"):
        end = content.find("---", 3)
        if end == -1:
            return content, "", "yaml"
        return content[3:end].strip(), content[end + 3:].strip(), "yaml"
    return "", content, "none"


def build_qmd(meta: dict, slug: str, has_bib: bool) -> str:
    title = meta.get("title", "Untitled")
    date = str(meta.get("date", ""))[:10]
    authors = meta.get("authors", meta.get("author", []))
    if isinstance(authors, str):
        authors = [authors]
    pub_type_codes = meta.get("publication_types", ["2"])
    if isinstance(pub_type_codes, str):
        pub_type_codes = [pub_type_codes]
    categories = [PUB_TYPE_MAP.get(str(c), str(c)) for c in pub_type_codes]
    abstract = (meta.get("abstract") or "").strip()
    # Clean up abstract: remove leading/trailing quotes, collapse whitespace
    abstract = re.sub(r'\s+', ' ', abstract).strip()
    doi_raw = (meta.get("doi") or "").strip()
    doi = strip_doi_prefix(doi_raw) if doi_raw else ""
    journal = (meta.get("publication") or "").strip()
    url_pdf = (meta.get("url_pdf") or "").strip()
    featured = bool(meta.get("featured", False))

    year = date[:4] if date else ""

    # Build frontmatter as a dict and use yaml.dump for safe serialisation
    fm_dict = {"title": title, "date": date}
    if authors:
        fm_dict["author"] = authors
    if categories:
        fm_dict["categories"] = categories
    if abstract:
        fm_dict["abstract"] = abstract
    if doi:
        fm_dict["doi"] = doi
    if journal:
        fm_dict["publication"] = journal
    if url_pdf and url_pdf != doi_raw:
        fm_dict["url_pdf"] = url_pdf.strip()
    if featured:
        fm_dict["featured"] = True

    fm_yaml = yaml.dump(fm_dict, allow_unicode=True, default_flow_style=False,
                        sort_keys=False, width=120)
    fm = "---\n" + fm_yaml + "---"

    # Build body
    authors_display = ", ".join(authors) if authors else ""
    journal_display = journal if journal else ""

    body_parts = []

    if featured:
        body_parts.append('<div class="pub-badge">Featured</div>\n')

    body_parts.append(f"## {title}\n")
    body_parts.append(f'<p class="pub-meta">{authors_display}</p>\n')

    if journal_display or year:
        cite_parts = []
        if journal_display:
            cite_parts.append(f"_{journal_display}_")
        if year:
            cite_parts.append(year)
        body_parts.append(", ".join(cite_parts) + "\n")

    if abstract:
        body_parts.append(f'\n<div class="pub-abstract">\n{abstract}\n</div>\n')

    links = []
    if doi:
        links.append(f'<a href="https://doi.org/{doi}" class="btn btn-primary btn-sm" target="_blank">'
                     f'<i class="bi bi-box-arrow-up-right"></i> DOI</a>')
    if url_pdf and url_pdf.startswith("http"):
        links.append(f'<a href="{url_pdf}" class="btn btn-outline-secondary btn-sm" target="_blank">'
                     f'<i class="bi bi-file-pdf"></i> PDF</a>')
    if has_bib:
        links.append(f'<a href="{slug}.bib" class="btn btn-outline-secondary btn-sm">'
                     f'<i class="bi bi-download"></i> BibTeX</a>')

    if links:
        body_parts.append('\n<div class="pub-links">\n' + "\n".join(links) + "\n</div>\n")

    body = "\n".join(body_parts)
    return fm + "\n\n" + body


def convert_all():
    if not SRC_DIR.exists():
        print(f"Source directory not found: {SRC_DIR}")
        return

    DST_DIR.mkdir(exist_ok=True)
    count = 0
    errors = []

    for pub_dir in sorted(SRC_DIR.iterdir()):
        if not pub_dir.is_dir():
            continue
        slug = pub_dir.name
        src_index = pub_dir / "index.md"
        if not src_index.exists():
            continue

        try:
            content = src_index.read_text(encoding="utf-8")
            fm_str, body, fmt = split_frontmatter(content)

            if fmt == "toml":
                meta = parse_toml_fm(fm_str)
            elif fmt == "yaml":
                meta = parse_yaml_fm(fm_str)
            else:
                meta = {}

            dst_pub_dir = DST_DIR / slug
            dst_pub_dir.mkdir(exist_ok=True)

            bib_src = pub_dir / f"{slug}.bib"
            has_bib = bib_src.exists()
            if has_bib:
                shutil.copy2(bib_src, dst_pub_dir / f"{slug}.bib")

            for img_name in ["featured.png", "featured.jpg", "featured.jpeg"]:
                img_src = pub_dir / img_name
                if img_src.exists():
                    shutil.copy2(img_src, dst_pub_dir / img_name)

            qmd_content = build_qmd(meta, slug, has_bib)
            (dst_pub_dir / "index.qmd").write_text(qmd_content, encoding="utf-8")
            count += 1

        except Exception as e:
            errors.append((slug, str(e)))
            print(f"  ERROR {slug}: {e}")

    print(f"\nConverted {count} publications to {DST_DIR}")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for slug, err in errors:
            print(f"  {slug}: {err}")


if __name__ == "__main__":
    convert_all()
