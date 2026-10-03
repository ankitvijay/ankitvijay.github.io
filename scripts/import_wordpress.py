#!/usr/bin/env python3
"""Import a public WordPress.com site into this Hugo repository.

Reads posts, pages and comments from the public WordPress.com REST API,
downloads every referenced image, converts post HTML to Markdown and writes:

  content/posts/YYYY-MM-DD-slug.md
  content/<page-slug>.md
  data/comments/p<post id>.json
  data/terms.json                      (category/tag display names)
  static/wp-content/uploads/YYYY/MM/<file>

Usage:
  python scripts/import_wordpress.py                 # live import
  WP_FIXTURE=dir python scripts/import_wordpress.py   # offline test from JSON files

Requires: beautifulsoup4, markdownify
"""
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from markdownify import MarkdownConverter

SITE = os.environ.get("WP_SITE", "ankitvijay.net")
FILES_HOST = os.environ.get("WP_FILES_HOST", "ankitvijaydotin.files.wordpress.com")
API = f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE}"
FIXTURE = os.environ.get("WP_FIXTURE")
ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "wp-to-hugo-import/1.0"}

# Any URL that points at the media library, whichever host serves it.
MEDIA_RE = re.compile(
    r"https?://(?:i\d\.wp\.com/)?(?:"
    + re.escape(SITE) + r"/wp-content/uploads|"
    + re.escape(FILES_HOST) + r"|"
    r"[a-z0-9-]+\.files\.wordpress\.com)"
    r"/(\d{4}/\d{2}/[^\s\"'?)<>]+)(\?[^\s\"')<>]*)?",
    re.I,
)
LANG_MAP = {
    "jscript": "javascript", "js": "javascript", "plain": "", "text": "",
    "c#": "csharp", "cs": "csharp", "ps": "powershell", "shell": "bash",
    "html": "html", "xml": "xml", "yml": "yaml",
}
warnings = []
media = set()


def warn(msg):
    warnings.append(msg)
    print(f"  WARNING: {msg}")


def get_json(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except (urllib.error.URLError, TimeoutError) as e:
            if isinstance(e, urllib.error.HTTPError) and e.code in (401, 403, 404):
                raise
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Could not fetch {url}")


def fetch_items(kind):
    """kind is 'post' or 'page'."""
    if FIXTURE:
        p = Path(FIXTURE) / f"{kind}s.json"
        return json.loads(p.read_text()) if p.exists() else []
    items, page = [], 1
    while True:
        data = get_json(f"{API}/posts/?type={kind}&status=publish&number=100&page={page}")
        batch = data.get("posts", [])
        items += batch
        print(f"  fetched {len(items)}/{data.get('found', '?')} {kind}s")
        if len(batch) < 100:
            return items
        page += 1


def fetch_comments():
    if FIXTURE:
        p = Path(FIXTURE) / "comments.json"
        return json.loads(p.read_text()) if p.exists() else []
    items, offset = [], 0
    try:
        while True:
            data = get_json(f"{API}/comments/?status=approved&type=comment&number=100&offset={offset}")
            batch = data.get("comments", [])
            items += batch
            if len(batch) < 100:
                return items
            offset += 100
    except Exception as e:  # comments are optional; never fail the import over them
        warn(f"comments could not be fetched ({e}); continuing without them")
        return items


def localise_media(text):
    """Point media URLs at /wp-content/uploads/... and remember them for download."""
    def repl(m):
        path = m.group(1).rstrip(".,;")
        media.add(path)
        return "/wp-content/uploads/" + path
    return MEDIA_RE.sub(repl, text or "")


def code_language(tag):
    classes = " ".join(tag.get("class", []))
    code = tag.find("code")
    if code is not None:
        classes += " " + " ".join(code.get("class", []))
    m = re.search(r"brush:\s*([\w#+-]+)", classes) or re.search(r"language-([\w#+-]+)", classes)
    lang = (tag.get("data-lang") or (m.group(1) if m else "")).lower()
    return LANG_MAP.get(lang, lang)


class Converter(MarkdownConverter):
    def convert_pre(self, el, text, *args, **kwargs):
        code = el.get_text().replace("\r\n", "\n").strip("\n")
        fence = "```"
        while fence in code:
            fence += "`"
        return f"\n\n{fence}{code_language(el)}\n{code}\n{fence}\n\n"


def to_markdown(content_html, where):
    soup = BeautifulSoup(localise_media(content_html), "html.parser")
    raw = []

    def keep_raw(node, markup=None):
        raw.append(markup if markup is not None else str(node))
        node.replace_with(NavigableString(f"\n\nRAWHTMLBLOCK{len(raw) - 1}END\n\n"))

    # WordPress.com decorations that are not part of the post.
    for sel in ["script", "style", ".sharedaddy", "#jp-post-flair", ".wpcnt", ".jp-relatedposts",
                ".wp-block-jetpack-subscriptions", ".wp-block-jetpack-like", "form"]:
        for node in soup.select(sel):
            src = node.get("src", "") if node.name == "script" else ""
            if "gist.github.com" in src:
                keep_raw(node, f'<script src="{src}"></script>')
            else:
                node.decompose()

    for node in soup.select("div.gist-oembed, [data-gist]"):
        gist = node.get("data-gist", "").replace(".json", ".js")
        if gist:
            keep_raw(node, f'<script src="https://gist.github.com/{gist}"></script>')

    for node in soup.find_all(["iframe", "video", "audio"]):
        for attr in ("src", "data-src"):
            if node.get(attr, "").startswith("//"):
                node[attr] = "https:" + node[attr]
        keep_raw(node, f'<div class="embed">{node}</div>' if node.name == "iframe" else None)

    for node in soup.select("blockquote.twitter-tweet"):
        keep_raw(node)

    # Embeds that are only a bare URL (unrendered oEmbed) become plain links.
    for node in soup.select("figure.wp-block-embed, .wp-block-embed__wrapper"):
        if node.parent is None:
            continue
        text = node.get_text(strip=True)
        if re.fullmatch(r"https?://\S+", text) and not node.find("a"):
            link = soup.new_tag("a", href=text)
            link.string = text
            para = soup.new_tag("p")
            para.append(link)
            node.replace_with(para)

    for img in soup.find_all("img"):
        for attr in ("srcset", "sizes", "loading", "decoding", "data-attachment-id"):
            img.attrs.pop(attr, None)
        if img.get("data-orig-file") and not img.get("src"):
            img["src"] = img["data-orig-file"]

    # <figure><img><figcaption> becomes an image followed by an italic caption.
    for fig in soup.find_all("figure"):
        if fig.parent is None or fig.find("table"):
            continue
        cap = fig.find("figcaption")
        caption = cap.get_text(" ", strip=True) if cap else ""
        if cap:
            cap.decompose()
        if caption:
            em = soup.new_tag("em")
            em.string = caption
            para = soup.new_tag("p")
            para.append(em)
            fig.insert_after(para)
        fig.name = "p"
        fig.attrs = {}

    for a in soup.find_all("a", href=True):
        a["href"] = re.sub(rf"^https?://(www\.)?{re.escape(SITE)}/", "/", a["href"])

    md = Converter(heading_style="ATX", bullets="-", escape_asterisks=False,
                   escape_underscores=False, strip=["span"]).convert_soup(soup)
    md = re.sub(r"RAWHTMLBLOCK(\d+)END", lambda m: raw[int(m.group(1))], md)
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"

    # Hugo would try to run {{< ... >}} / {{% ... %}} as shortcodes; show them literally instead.
    md, n = re.subn(r"\{\{([<%])(.*?)([>%])\}\}", r"{{\1/*\2*/\3}}", md, flags=re.S)
    if n:
        warn(f"{where}: escaped {n} shortcode-like sequence(s); check they display correctly")
    if "{{<" in md.replace("{{</*", "") or "{{%" in md.replace("{{%/*", ""):
        warn(f"{where}: contains an unmatched '{{{{<' or '{{{{%' that may break the build")
    return md


def clean_text(value):
    return re.sub(r"\s+", " ", html.unescape(value or "").replace("\xa0", " ")).strip()


def front_matter(fields):
    lines = ["---"]
    for key, value in fields.items():
        if value in (None, "", []):
            continue
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    return "\n".join(lines) + "\n---\n\n"


term_names = {"category": {}, "tag": {}}


def terms(mapping, taxonomy):
    """Return WordPress term slugs (so archive addresses stay the same) and remember display names."""
    slugs = []
    for name, t in (mapping or {}).items():
        label = clean_text(t.get("name") or name)
        slug = (t.get("slug") or re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-") or "misc").lower()
        term_names[taxonomy][slug] = label
        slugs.append(slug)
    return sorted(slugs)


def write_item(item, kind):
    path = urllib.parse.urlparse(item["URL"]).path
    if not path.endswith("/"):
        path += "/"
    slug = item.get("slug") or path.strip("/").split("/")[-1]
    where = f"{kind} {path}"
    if kind == "page" and path == "/":
        print(f"  skipping front page ({item.get('title')})")
        return None
    excerpt = clean_text(BeautifulSoup(item.get("excerpt") or "", "html.parser").get_text(" "))
    excerpt = re.sub(r"\s*(\[…\]|\[&hellip;\]|Read more.*)$", "", excerpt)
    fields = {
        "title": clean_text(item.get("title")) or slug,
        "date": item["date"],
        "lastmod": item.get("modified"),
        "url": path,
        "slug": slug,
        "wp_id": item["ID"],
    }
    if kind == "post":
        fields["category"] = terms(item.get("categories"), "category")
        fields["tag"] = terms(item.get("tags"), "tag")
        fields["summary"] = excerpt
        fields["featured_image"] = localise_media(item.get("featured_image") or "")
        out = ROOT / "content" / "posts" / f"{item['date'][:10]}-{slug}.md"
    else:
        fields["layout"] = "page"
        out = ROOT / "content" / f"{slug}.md"
    body = to_markdown(item.get("content") or "", where)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(front_matter(fields) + body, encoding="utf-8")
    return item["ID"]


def write_comments(comments, known_ids):
    by_post = {}
    for c in comments:
        post_id = (c.get("post") or {}).get("ID")
        if post_id not in known_ids:
            continue
        author = c.get("author") or {}
        parent = c.get("parent") or {}
        by_post.setdefault(post_id, []).append({
            "id": c["ID"],
            "author": clean_text(author.get("name")) or "Anonymous",
            "author_url": author.get("URL") or "",
            "date": c.get("date"),
            "parent": parent.get("ID", 0) if isinstance(parent, dict) else 0,
            "content": localise_media(c.get("content") or ""),
        })
    out_dir = ROOT / "data" / "comments"
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("p*.json"):
        old.unlink()
    for post_id, items in by_post.items():
        items.sort(key=lambda c: c["date"] or "")
        (out_dir / f"p{post_id}.json").write_text(
            json.dumps(items, indent=1, ensure_ascii=False), encoding="utf-8")
    return sum(len(v) for v in by_post.values())


def download_media():
    ok = failed = skipped = 0
    for path in sorted(media):
        dest = ROOT / "static" / "wp-content" / "uploads" / urllib.parse.unquote(path)
        if dest.exists() and dest.stat().st_size > 0:
            skipped += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        for url in (f"https://{FILES_HOST}/{path}", f"https://{SITE}/wp-content/uploads/{path}"):
            try:
                req = urllib.request.Request(url, headers=UA)
                with urllib.request.urlopen(req, timeout=120) as r:
                    dest.write_bytes(r.read())
                ok += 1
                break
            except Exception:
                continue
        else:
            failed += 1
            warn(f"could not download media {path}")
    return ok, skipped, failed


def main():
    print(f"Importing {SITE}" + (f" (fixture: {FIXTURE})" if FIXTURE else ""))
    posts, pages = fetch_items("post"), fetch_items("page")
    if not posts:
        sys.exit("No posts were returned; nothing imported.")
    for old in (ROOT / "content" / "posts").glob("*.md"):
        old.unlink()
    ids = {write_item(p, "post") for p in posts}
    page_count = sum(1 for p in pages if write_item(p, "page"))
    comment_count = write_comments(fetch_comments(), ids)
    (ROOT / "data" / "terms.json").write_text(
        json.dumps(term_names, indent=1, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    ok, skipped, failed = (0, 0, 0) if FIXTURE else download_media()

    summary = [
        "## WordPress import summary", "",
        f"- Posts: {len(posts)}", f"- Pages: {page_count}", f"- Comments: {comment_count}",
        f"- Media referenced: {len(media)} (downloaded {ok}, already present {skipped}, failed {failed})",
        f"- Warnings: {len(warnings)}", "",
    ] + [f"  - {w}" for w in warnings]
    text = "\n".join(summary)
    print("\n" + text)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(text + "\n")
    (ROOT / "import-report.md").write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
