# ankitvijay.net

Source for [ankitvijay.net](https://ankitvijay.net), built with [Hugo](https://gohugo.io) and published with GitHub Pages.

## How it works

- `content/posts/` – one Markdown file per blog post. The `url` in each file's header keeps the address the post had on WordPress.
- `content/*.md` – standalone pages (About, Contact, ...).
- `static/wp-content/uploads/` – images, at the same addresses WordPress used.
- `data/comments/` – comments carried over from WordPress (read-only).
- `layouts/`, `static/css/style.css` – the site's templates and styling.

Every push to the default branch rebuilds and publishes the site (`.github/workflows/deploy.yml`).

## Writing a post

Add a file such as `content/posts/2026-10-03-my-post.md`:

```markdown
---
title: "My post"
date: "2026-10-03T09:00:00+10:00"
url: "/2026/10/03/my-post/"
category: ["net"]
tag: ["c-sharp"]
summary: "One sentence shown on the home page."
---

Post text in Markdown.
```

Preview locally with `hugo server`.

## Re-importing from WordPress

Actions tab → **Import from WordPress** → **Run workflow**. It re-reads every post, page, comment and image from the WordPress.com site and commits the result, replacing the files in `content/posts/`. Only needed during the migration.
