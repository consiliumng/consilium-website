# consilium.ng — Eleventy + Decap CMS rebuild

This replaces the flat-HTML site with an Eleventy-generated one. The design,
copy, and URLs are unchanged — what changed is how the files are organized
and how new content gets added.

## What's different from the old flat-HTML site

- **One shared layout** (`_includes/base.njk`) instead of nav/footer copy-pasted
  into six files.
- **Reports and posts live in `content/reports/` and `content/posts/`** —
  one small file per report or post — instead of being hardcoded inside
  `<script>` tags or fetched from Google Sheets at page-load time.
- **Every report is a real page** (`/reports/<slug>/`), generated at build
  time from `reports.njk`, with its own title and social-preview image —
  replacing the old single `report.html` + `_redirects` rewrite trick.
- **Decap CMS is wired in** (`/admin`) — once Netlify Identity + Git
  Gateway are turned on (see below), you get a real editor for reports and
  posts instead of hand-editing files or a spreadsheet.

## Three bugs found in the old site and fixed here

1. The homepage's featured posts were a hardcoded array that could drift
   out of sync with the Writing page's live-fetched posts. Now both pull
   from the same `posts` collection — there's only one list.
2. The "Download" button on the Research hub page called a JavaScript
   function (`openDownload`) that was never defined anywhere — clicking it
   silently did nothing. Fixed by linking to the report's own page, where
   the real, working download gate lives.
3. The newsletter signup form (`nlSubscribe`) was implemented three
   different, inconsistent ways across pages, and wasn't defined at all on
   `research.html` or `writing.html` — meaning that footer form was broken
   on two of six pages. Now there's one shared, working implementation.

## Names and addresses (updated October 2026)

The site uses **Reports** and **Articles** everywhere (menu, breadcrumbs, page
titles, footer, CMS). The old words "Research" and "Writing" are retired.

| Page | Address | Built from |
|---|---|---|
| Reports list | `/reports/` | `reports-index.njk` |
| One report | `/reports/<slug>/` | `reports.njk` |
| Articles list | `/articles/` | `articles-index.njk` |
| One article | `/articles/<slug>/` | `articles.njk` |
| One author | `/authors/<slug>/` | `authors.njk` |

The old addresses (`/research`, `/research.html`, `/writing`, `/writing.html`)
forward to the new ones through the redirect rules in `netlify.toml`.

The **Articles** page and the homepage merge native articles and Substack link
posts into one newest-first feed (`collections.articlesFeed` in
`eleventy.config.js`). Visitors never see the difference.

All internal links are written from the site root (`/reports/`, not
`reports.html`), so they work from any page depth.

Plain `.html` files (the `/admin` page and interactive explainers such as
`/reports/us-nigeria-mou/`) are copied through untouched. Only `.njk` and `.md`
files are templates (`templateFormats` in `eleventy.config.js`).

## Authors

People live in `content/authors/` (CMS section **Authors**). Reports, articles
and Substack links each have an **Authors** picker. A name then appears on the
page and links to that person's page at `/authors/<slug>/`, which lists
everything they have written. A person's page is built only once they have at
least one published item. Items with no author fall back to the plain text
"Consilium Research" on report pages.

## Content model

Three collections, all managed through the CMS at `/admin`:

- **Reports** (`content/reports/`) — one Markdown file per report. Fields
  include title, tag, stats, key findings, an optional table of contents,
  optional preview figures, optional methodology (see below), and a PDF
  file for the download gate.
- **Articles** (`content/articles/`) — one Markdown file per native,
  on-site long-form piece. Full rich-text body (supports embedded images
  and pull-quotes), auto-generated table of contents from your `##`
  headings, key takeaways, author, and SEO fields.
- **Posts** (`content/posts/`) — short entries that link out to an
  external Substack post. The Writing page and homepage both merge Posts
  and Articles into one date-sorted feed automatically (see
  `collections.writing` in `eleventy.config.js`) — visitors never see a
  difference between the two types.

**Currently migrated:** the 2 reports and 3 posts that were embedded as
fallback data in the old site's code. The live Google Sheets weren't
reachable from the environment this was built in — if they contain more
entries than what's here, add them through the CMS following the same
format. The 3 existing posts are kept as external Substack links rather
than converted to native Articles, since their real full-length text
was never available to migrate — only teasers.

**Methodology is optional.** Reports like financial valuations that don't
have a research methodology can simply leave that field blank in the CMS
— the whole section is conditional and disappears cleanly.

## The report download gate

Every report with "Offer a PDF download?" turned on shows a gated
download form (name, email, organisation, optional newsletter opt-in).
On submit, it POSTs to your existing Apps Script endpoint
(`PARTNERSHIP_SCRIPT_URL` in `reports.njk`) with the report's slug,
title, and PDF link — the link and title come straight from the CMS's
"PDF file" and "Title" fields on that report, nothing hardcoded and
nothing to keep in sync manually anywhere.

**This builds on an Apps Script backend you already had** (it already
handled `type: 'download'`, partnership enquiries, Brevo email with a
Gmail fallback, and its own Report Downloads / Partnership Leads / Error
Log sheets, auto-created if missing). Two small updates were made to
your existing script — see `apps-script-cms-update.gs`, delivered
separately, for the exact functions to replace:

1. `handleDownload()` now reads the PDF link and title directly from
   the incoming request (i.e. from the CMS) instead of looking them up
   in a separate "Report Links" sheet tab. That sheet and its lookup
   function (`getReportData`) are no longer used — safe to delete, or
   leave in place, your call.
2. `sendViaBrevo()` now reads the Brevo API key from Script Properties
   instead of a hardcoded constant in the file. **Important:** the old
   key was pasted into a chat conversation at one point, so treat it as
   exposed — revoke it in Brevo and generate a new one, then store the
   new one via Project Settings → Script Properties → `BREVO_API_KEY`.

**Fill in the "PDF file" field on the HCW 2025 report in the CMS** —
it currently has downloads switched on but no file attached yet, so
submissions will log correctly but no email will send until that's
added.

**Known limitation:** the frontend calls this endpoint with
`mode: 'no-cors'`, so the browser can't confirm the request actually
succeeded server-side — the success message shows optimistically. The
Report Downloads sheet (or Brevo's own send log) is the real record of
whether an email actually went out.

**Uploaded files (PDFs, cover images, preview figures) are served from
`content/uploads/`** — `eleventy.config.js` explicitly copies that
folder into the built site. Without that passthrough, anything uploaded
through the CMS would 404 on the live site; this was fixed as part of
this change.

**Metrics**, three layers: the Downloads Sheet (who downloaded what,
when), Brevo's dashboard (did they open/click the email), and a GA4
`report_download` event fired client-side on success, tagged with the
report's slug and title — giving you a full funnel in Google Analytics,
not just a raw total.

## Local development

```
npm install
npx @11ty/eleventy --serve
```

## Deploying

Netlify build settings:
- Build command: `npx @11ty/eleventy`
- Publish directory: `_site`

(Already set in `netlify.toml` — Netlify will pick this up automatically
once the repo is linked.)

## Turning on the CMS

1. In Netlify: Site configuration → Identity → Enable Identity → set
   registration to "Invite only."
2. Identity → Services → enable Git Gateway.
3. Identity → Invite users → invite yourself.
4. **Build & deploy → Deploy contexts → Branch deploys → set to "All"
   (or "Let me add individual branches" and add `cms/*`).** This is
   required for step 5 below — without it, preview links won't work.
5. Visit `consilium.ng/admin`, log in, and start editing.

### Editorial Workflow (draft → preview → publish)

`publish_mode: editorial_workflow` is set in `admin/config.yml`, so
entries don't publish instantly. Instead: save as a draft, open it
again, and a "Preview" link appears in the editor — that opens the
real, fully-styled page (built by Netlify from that draft's branch,
per step 4 above) before it's live. Move the entry to "Ready" to
actually publish it. All of this happens inside `/admin` — nothing
moves to a different interface, it just adds a small board view
(Drafts → In Review → Ready) instead of one flat list.

## Analytics

Google Analytics (`G-VVY7VZZE79`) is in the shared layout's `<head>` —
one place, applies to every page automatically. The `report_download`
event (see above) is the one custom event currently wired up.
