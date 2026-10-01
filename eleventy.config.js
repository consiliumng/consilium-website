module.exports = function (eleventyConfig) {
  // Static passthrough — files Netlify should serve as-is
  eleventyConfig.addPassthroughCopy("og-image.png");
  eleventyConfig.addPassthroughCopy("reports/us-nigeria-mou");
  eleventyConfig.addPassthroughCopy("admin");
  // CMS-uploaded images and PDFs (cover images, preview figures, report
  // PDFs) land here — without this, every file uploaded through the CMS
  // would 404 on the live site.
  eleventyConfig.addPassthroughCopy({ "content/uploads": "content/uploads" });
  eleventyConfig.ignores.add("README.md");

  // REPORTS collection — one entry per file in content/reports/
  // sorted newest first. This replaces the REPORTS_CSV_URL fetch +
  // FALLBACK_REPORTS duplication that used to live in index.html,
  // research.html, and report.html separately.
  eleventyConfig.addCollection("reports", function (collectionApi) {
    return collectionApi.getFilteredByGlob("content/reports/*.md")
      .filter((item) => item.data.published !== false)
      .sort((a, b) => (b.data.date || 0) - (a.data.date || 0));
  });

  // POSTS collection — one entry per file in content/posts/,
  // sorted newest first. Used by BOTH index.html (top 3) and
  // writing.html (all) so there is exactly one source of truth —
  // fixes the drift where index.html had a hardcoded array that
  // could fall out of sync with the live posts.
  eleventyConfig.addCollection("posts", function (collectionApi) {
    return collectionApi.getFilteredByGlob("content/posts/*.md")
      .filter((item) => item.data.published !== false)
      .sort((a, b) => (b.data.date || 0) - (a.data.date || 0));
  });

  // ARTICLES collection — one entry per file in content/articles/,
  // sorted newest first. Full native long-form pieces, distinct from
  // "posts" (external Substack links).
  eleventyConfig.addCollection("articles", function (collectionApi) {
    return collectionApi.getFilteredByGlob("content/articles/*.md")
      .filter((item) => item.data.published !== false)
      .sort((a, b) => (b.data.date || 0) - (a.data.date || 0));
  });

  // ------------------------------------------------------------------
  // AUTHORS
  // One small file per person in content/authors/. Reports, articles and
  // posts point at people by slug (the "authors" list in each file), so a
  // name on any page can link to that person's page at /authors/<slug>/.
  // ------------------------------------------------------------------
  function toList(v) {
    if (v === undefined || v === null || v === "") return [];
    return Array.isArray(v) ? v : [v];
  }
  function isPublished(item) {
    return item.data.published !== false;
  }
  function byDateDesc(a, b) {
    return new Date(b.date || 0) - new Date(a.date || 0);
  }

  eleventyConfig.addCollection("authors", function (collectionApi) {
    return collectionApi.getFilteredByGlob("content/authors/*.md")
      .filter(isPublished)
      .sort((a, b) => (a.data.name || "").localeCompare(b.data.name || ""));
  });

  // ARTICLES FEED — what visitors see as "Articles": the native on-site
  // articles AND the Substack link posts, merged and sorted newest first.
  function buildArticlesFeed(collectionApi) {
    const posts = collectionApi.getFilteredByGlob("content/posts/*.md")
      .filter(isPublished)
      .map((i) => ({
        kind: "post", title: i.data.title, tag: i.data.tag, teaser: i.data.teaser,
        date: i.data.date, url: i.data.url, external: true, authors: toList(i.data.authors),
      }));
    const articles = collectionApi.getFilteredByGlob("content/articles/*.md")
      .filter(isPublished)
      .map((i) => ({
        kind: "article", title: i.data.title, tag: i.data.tag, teaser: i.data.teaser,
        date: i.data.date, url: "/articles/" + i.data.slug + "/", external: false,
        authors: toList(i.data.authors),
      }));
    return posts.concat(articles).sort(byDateDesc);
  }
  eleventyConfig.addCollection("articlesFeed", buildArticlesFeed);

  // AUTHOR PAGES — one page per person who has at least one published
  // report, article or post. Lists everything they have written.
  eleventyConfig.addCollection("authorPages", function (collectionApi) {
    const reports = collectionApi.getFilteredByGlob("content/reports/*.md")
      .filter(isPublished)
      .map((i) => ({
        kind: "report", title: i.data.title, tag: i.data.tag, teaser: i.data.description,
        date: i.data.date, url: "/reports/" + i.data.slug + "/", external: false,
        authors: toList(i.data.authors),
      }));
    const everything = buildArticlesFeed(collectionApi).concat(reports).sort(byDateDesc);
    return collectionApi.getFilteredByGlob("content/authors/*.md")
      .filter(isPublished)
      .map((a) => ({
        slug: a.data.slug, name: a.data.name, role: a.data.role,
        bio: a.data.bio, photo: a.data.photo,
        items: everything.filter((it) => it.authors.indexOf(a.data.slug) !== -1),
      }))
      .filter((a) => a.items.length > 0);
  });

  // Turns a list of author slugs into the matching author records.
  eleventyConfig.addFilter("resolveAuthors", function (slugs, authorItems) {
    const map = {};
    (authorItems || []).forEach((a) => { map[a.data.slug] = a.data; });
    return toList(slugs).map((s) => map[s]).filter(Boolean);
  });

  // "A", "A and B", "A, B and C" — plain text, for cards (which are
  // links themselves, so names there cannot be links too).
  eleventyConfig.addFilter("authorNames", function (slugs, authorItems) {
    const map = {};
    (authorItems || []).forEach((a) => { map[a.data.slug] = a.data.name; });
    const names = toList(slugs).map((s) => map[s]).filter(Boolean);
    if (names.length <= 1) return names.join("");
    return names.slice(0, -1).join(", ") + " and " + names[names.length - 1];
  });

  // Two-letter initials for avatars, skipping titles like "Dr."
  eleventyConfig.addFilter("initials", function (name) {
    const parts = String(name || "")
      .replace(/\b(Dr|Prof|Mr|Mrs|Ms)\.?\s/gi, "")
      .trim().split(/\s+/).filter(Boolean);
    if (!parts.length) return "";
    const first = parts[0][0];
    const last = parts.length > 1 ? parts[parts.length - 1][0] : "";
    return (first + last).toUpperCase();
  });

  // Counts items whose attribute equals a value. Works on collection items
  // (path "data.tag") and on plain objects (path "tag"). Nunjucks' own
  // selectattr cannot do this, which made the filter-button counts wrong.
  eleventyConfig.addFilter("countBy", function (items, path, value) {
    const keys = String(path).split(".");
    return (items || []).filter((it) => {
      let v = it;
      for (const k of keys) { v = v == null ? v : v[k]; }
      return v === value;
    }).length;
  });

  // Simple year formatter — used on post cards (Writing page)
  eleventyConfig.addFilter("date", function (dateValue, fmt) {
    if (!dateValue) return "";
    const d = new Date(dateValue);
    if (fmt === "yyyy") return String(d.getFullYear());
    return d.toISOString();
  });

  // slugify — used by the two heading filters below
  function slugify(text) {
    return text.toLowerCase().trim()
      .replace(/[^\w\s-]/g, "")
      .replace(/\s+/g, "-");
  }

  // Injects an id="" onto every <h2> in a rendered article body, so the
  // table-of-contents links below can jump straight to that section.
  eleventyConfig.addFilter("withHeadingIds", function (html) {
    if (!html) return html;
    return html.replace(/<h2>(.*?)<\/h2>/g, function (match, inner) {
      const id = slugify(inner.replace(/<[^>]+>/g, ""));
      return '<h2 id="' + id + '">' + inner + "</h2>";
    });
  });

  // Pulls the same <h2> headings out as a plain list, for the sticky
  // "On this page" table of contents.
  eleventyConfig.addFilter("extractHeadings", function (html) {
    if (!html) return [];
    const headings = [];
    const re = /<h2>(.*?)<\/h2>/g;
    let m;
    while ((m = re.exec(html)) !== null) {
      const text = m[1].replace(/<[^>]+>/g, "");
      headings.push({ text: text, id: slugify(text) });
    }
    return headings;
  });

  return {
    dir: {
      input: ".",
      includes: "_includes",
      output: "_site",
    },
    // Only .njk and .md files are treated as templates. Plain .html files
    // (the /admin page and the interactive explainers under /reports/) are
    // copied exactly as they are, never run through the template engine.
    templateFormats: ["njk", "md"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
  };
};
