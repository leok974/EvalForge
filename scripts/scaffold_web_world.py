# scripts/scaffold_web_world.py
from __future__ import annotations
from pathlib import Path
import argparse
import json

REJECT_TODO = True

ROOT = Path(__file__).resolve().parents[1]
DATA_QUESTS = ROOT / "data" / "quests"

HTML_SPECS = [
  ("html-ignition", "HTML Ignition: Page Skeleton",
"""# HTML Ignition: Page Skeleton

Edit `index.html`.

Requirements:
1) First line: `<!DOCTYPE html>`
2) `<html lang="en">`
3) `<head>` includes:
   - `<meta charset="utf-8">`
   - `<meta name="viewport" content="width=device-width, initial-scale=1">`
   - `<title>EvalForge HTML</title>`
4) `<main data-testid="app">Hello, Web</main>` exists in `<body>`.
""",
"<!DOCTYPE html>\n<html>\n<body>\n  <div id='app'>TODO</div>\n</body>\n</html>\n",
"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n  <title>EvalForge HTML</title>\n</head>\n<body>\n  <main data-testid=\"app\">Hello, Web</main>\n</body>\n</html>\n",
r"""
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  readText, normLF, compactWS, assertNoTodo, assertMatches, assertTagText, findOpenTag, hasAttr
} from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("html-ignition: skeleton + app", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /^<!DOCTYPE html>\n/i, "doctype must be first line");
  const openHtml = findOpenTag(html, "html");
  hasAttr(openHtml, "lang", "en");
  assertMatches(html, /<meta\s+charset=["']utf-8["']\s*\/?>/i, "meta charset utf-8");
  assertMatches(html, /<meta\s+name=["']viewport["']\s+content=["']width=device-width,\s*initial-scale=1["']\s*\/?>/i, "meta viewport");
  assertTagText(html, "title", "EvalForge HTML");
  assertMatches(html, /<main\b[^>]*data-testid=["']app["'][^>]*>[\s\S]*?<\/main>/i, "main data-testid=app");
  assertMatches(html, /<main\b[^>]*data-testid=["']app["'][^>]*>\s*Hello,\s*Web\s*<\/main>/i, "app text exact");
  assertNoTodo(html);
});
"""
),
  ("html-tags-attributes", "Tags & Attributes",
"""# Tags & Attributes

Edit `index.html`.

Requirements:
1) A `<header data-testid="header">` with `<h1>My Site</h1>`
2) A `<section id="profile" class="card" data-testid="profile">`
3) Inside section: `<p class="tagline">Building with HTML</p>`
4) A `<footer data-testid="footer">© 2026</footer>`
""",
"<!DOCTYPE html>\n<html lang=\"en\">\n<head><meta charset=\"utf-8\"><title>TODO</title></head>\n<body>TODO</body>\n</html>\n",
"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\">\n  <title>Tags & Attributes</title>\n</head>\n<body>\n  <header data-testid=\"header\"><h1>My Site</h1></header>\n  <section id=\"profile\" class=\"card\" data-testid=\"profile\">\n    <p class=\"tagline\">Building with HTML</p>\n  </section>\n  <footer data-testid=\"footer\">© 2026</footer>\n</body>\n</html>\n",
r"""
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("tags + attributes required", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<header\b[^>]*data-testid=["']header["'][^>]*>\s*<h1>\s*My Site\s*<\/h1>\s*<\/header>/i);
  assertMatches(html, /<section\b[^>]*id=["']profile["'][^>]*class=["'][^"']*\bcard\b[^"']*["'][^>]*data-testid=["']profile["'][^>]*>/i);
  assertMatches(html, /<p\b[^>]*class=["'][^"']*\btagline\b[^"']*["'][^>]*>\s*Building with HTML\s*<\/p>/i);
  assertMatches(html, /<footer\b[^>]*data-testid=["']footer["'][^>]*>\s*©\s*2026\s*<\/footer>/i);
  assertNoTodo(html);
});
"""
),
  ("html-links-images", "Links & Images",
"""# Links & Images

Edit `index.html`.

Requirements:
1) An `<a data-testid="docs-link">Docs</a>` with:
   - href="https://example.com/docs"
   - target="_blank"
   - rel includes "noopener"
2) An `<img data-testid="logo">` with:
   - src="assets/logo.png"
   - alt="EvalForge logo"
   - width="120" height="120"
""",
"<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"></head><body>TODO</body></html>\n",
"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\">\n  <title>Links & Images</title>\n</head>\n<body>\n  <a data-testid=\"docs-link\" href=\"https://example.com/docs\" target=\"_blank\" rel=\"noopener noreferrer\">Docs</a>\n  <img data-testid=\"logo\" src=\"assets/logo.png\" alt=\"EvalForge logo\" width=\"120\" height=\"120\" />\n</body>\n</html>\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("links + images", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<a\b[^>]*data-testid=["']docs-link["'][^>]*>\s*Docs\s*<\/a>/i);
  assertMatches(html, /<a\b[^>]*data-testid=["']docs-link["'][^>]*href=["']https:\/\/example\.com\/docs["']/i);
  assertMatches(html, /<a\b[^>]*data-testid=["']docs-link["'][^>]*target=["']_blank["']/i);
  assertMatches(html, /<a\b[^>]*data-testid=["']docs-link["'][^>]*rel=["'][^"']*noopener[^"']*["']/i);
  assertMatches(html, /<img\b[^>]*data-testid=["']logo["'][^>]*src=["']assets\/logo\.png["']/i);
  assertMatches(html, /<img\b[^>]*data-testid=["']logo["'][^>]*alt=["']EvalForge logo["']/i);
  assertMatches(html, /<img\b[^>]*data-testid=["']logo["'][^>]*width=["']120["'][^>]*height=["']120["']/i);
  assertNoTodo(html);
});
"""
),
  ("html-lists-tables", "Lists & Tables",
"""# Lists & Tables

Edit `index.html`.

Requirements:
1) `<ul data-testid="task-list">` with exactly 3 `<li>` items:
   - Learn
   - Build
   - Ship
2) `<table data-testid="scores">` with:
   - headers: Name, Score
   - rows: Alice 10; Bob 8
""",
"<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"></head><body>TODO</body></html>\n",
"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\">\n  <title>Lists & Tables</title>\n</head>\n<body>\n  <ul data-testid=\"task-list\">\n    <li>Learn</li>\n    <li>Build</li>\n    <li>Ship</li>\n  </ul>\n\n  <table data-testid=\"scores\">\n    <thead>\n      <tr><th>Name</th><th>Score</th></tr>\n    </thead>\n    <tbody>\n      <tr><td>Alice</td><td>10</td></tr>\n      <tr><td>Bob</td><td>8</td></tr>\n    </tbody>\n  </table>\n</body>\n</html>\n",
r"""
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("lists + tables", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<ul\b[^>]*data-testid=["']task-list["'][^>]*>[\s\S]*?<\/ul>/i);
  const m = html.match(/<ul\b[^>]*data-testid=["']task-list["'][^>]*>([\s\S]*?)<\/ul>/i);
  assert.ok(m, "task-list ul exists");
  const li = (m[1].match(/<li\b[^>]*>[\s\S]*?<\/li>/gi) || []).map(s => s.replace(/<[^>]+>/g,"").trim());
  assert.deepEqual(li, ["Learn","Build","Ship"]);

  assertMatches(html, /<table\b[^>]*data-testid=["']scores["'][^>]*>[\s\S]*?<\/table>/i);
  assertMatches(html, /<th>\s*Name\s*<\/th>\s*<th>\s*Score\s*<\/th>/i);
  assertMatches(html, /<td>\s*Alice\s*<\/td>\s*<td>\s*10\s*<\/td>/i);
  assertMatches(html, /<td>\s*Bob\s*<\/td>\s*<td>\s*8\s*<\/td>/i);
  assertNoTodo(html);
});
"""
),
  ("html-forms-inputs", "Forms & Inputs",
"""# Forms & Inputs

Edit `index.html`.

Requirements:
1) `<form data-testid="signup" action="/submit" method="post">`
2) Email field:
   - `<label for="email">Email</label>`
   - `<input id="email" name="email" type="email" required>`
3) Role select:
   - `<select id="role" name="role">` with options: student, mentor
4) `<button type="submit">Join</button>`
""",
"<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"></head><body>TODO</body></html>\n",
"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\">\n  <title>Forms & Inputs</title>\n</head>\n<body>\n  <form data-testid=\"signup\" action=\"/submit\" method=\"post\">\n    <label for=\"email\">Email</label>\n    <input id=\"email\" name=\"email\" type=\"email\" required />\n\n    <label for=\"role\">Role</label>\n    <select id=\"role\" name=\"role\">\n      <option value=\"student\">student</option>\n      <option value=\"mentor\">mentor</option>\n    </select>\n\n    <button type=\"submit\">Join</button>\n  </form>\n</body>\n</html>\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("forms + inputs", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<form\b[^>]*data-testid=["']signup["'][^>]*action=["']\/submit["'][^>]*method=["']post["'][^>]*>/i);
  assertMatches(html, /<label\b[^>]*for=["']email["'][^>]*>\s*Email\s*<\/label>/i);
  assertMatches(html, /<input\b[^>]*id=["']email["'][^>]*name=["']email["'][^>]*type=["']email["'][^>]*required/i);
  assertMatches(html, /<select\b[^>]*id=["']role["'][^>]*name=["']role["'][^>]*>[\s\S]*<\/select>/i);
  assertMatches(html, /<option\b[^>]*value=["']student["'][^>]*>\s*student\s*<\/option>/i);
  assertMatches(html, /<option\b[^>]*value=["']mentor["'][^>]*>\s*mentor\s*<\/option>/i);
  assertMatches(html, /<button\b[^>]*type=["']submit["'][^>]*>\s*Join\s*<\/button>/i);
  assertNoTodo(html);
});
"""
),
  ("html-semantic-layout", "Semantic Layout",
"""# Semantic Layout

Edit `index.html`.

Requirements:
1) Use semantic tags: header, nav, main, aside, footer
2) `nav` has `aria-label="Primary"`
3) `main` contains `<article data-testid="article"><h2>News</h2></article>`
""",
"<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"></head><body>TODO</body></html>\n",
"<!DOCTYPE html>\n<html lang=\"en\">\n<head><meta charset=\"utf-8\"><title>Semantic Layout</title></head>\n<body>\n  <header><h1>Portal</h1></header>\n  <nav aria-label=\"Primary\"><a href=\"#\">Home</a></nav>\n  <main>\n    <article data-testid=\"article\"><h2>News</h2></article>\n  </main>\n  <aside><p>Sidebar</p></aside>\n  <footer>Footer</footer>\n</body>\n</html>\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("semantic layout", () => {
  const html = normLF(readText(WS, "index.html"));
  for (const tag of ["header","nav","main","aside","footer"]) {
    assertMatches(html, new RegExp(`<${tag}\\b`, "i"), `missing <${tag}>`);
  }
  assertMatches(html, /<nav\b[^>]*aria-label=["']Primary["'][^>]*>/i);
  assertMatches(html, /<article\b[^>]*data-testid=["']article["'][^>]*>\s*<h2>\s*News\s*<\/h2>\s*<\/article>/i);
  assertNoTodo(html);
});
"""
),
  ("html-accessibility-basics", "Accessibility Basics",
"""# Accessibility Basics

Edit `index.html`.

Requirements:
1) `<img data-testid="avatar" ...>` must have non-empty alt text
2) `<button data-testid="close" aria-label="Close dialog">X</button>`
3) Form label + input pairing for `name`:
   - `<label for="name">Name</label>` and `<input id="name" name="name">`
""",
"<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"></head><body>TODO</body></html>\n",
"<!DOCTYPE html>\n<html lang=\"en\">\n<head><meta charset=\"utf-8\"><title>Accessibility</title></head>\n<body>\n  <img data-testid=\"avatar\" src=\"assets/avatar.png\" alt=\"User avatar\" />\n  <button data-testid=\"close\" aria-label=\"Close dialog\">X</button>\n\n  <form>\n    <label for=\"name\">Name</label>\n    <input id=\"name\" name=\"name\" />\n  </form>\n</body>\n</html>\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("accessibility basics", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<img\b[^>]*data-testid=["']avatar["'][^>]*alt=["'][^"']+["'][^>]*>/i, "img needs alt");
  assertMatches(html, /<button\b[^>]*data-testid=["']close["'][^>]*aria-label=["']Close dialog["'][^>]*>\s*X\s*<\/button>/i);
  assertMatches(html, /<label\b[^>]*for=["']name["'][^>]*>\s*Name\s*<\/label>/i);
  assertMatches(html, /<input\b[^>]*id=["']name["'][^>]*name=["']name["'][^>]*>/i);
  assertNoTodo(html);
});
"""
),
  ("html-media-embed", "Media & Embeds",
"""# Media & Embeds

Edit `index.html`.

Requirements:
1) `<video data-testid="demo-video" controls>` with `<source src="media/demo.mp4" type="video/mp4">`
2) `<iframe data-testid="embed" src="https://example.com/embed" title="Demo Embed"></iframe>`
""",
"<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"></head><body>TODO</body></html>\n",
"<!DOCTYPE html>\n<html lang=\"en\">\n<head><meta charset=\"utf-8\"><title>Media</title></head>\n<body>\n  <video data-testid=\"demo-video\" controls>\n    <source src=\"media/demo.mp4\" type=\"video/mp4\" />\n  </video>\n\n  <iframe data-testid=\"embed\" src=\"https://example.com/embed\" title=\"Demo Embed\"></iframe>\n</body>\n</html>\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("media + embeds", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<video\b[^>]*data-testid=["']demo-video["'][^>]*controls[^>]*>/i);
  assertMatches(html, /<source\b[^>]*src=["']media\/demo\.mp4["'][^>]*type=["']video\/mp4["'][^>]*\/?>/i);
  assertMatches(html, /<iframe\b[^>]*data-testid=["']embed["'][^>]*src=["']https:\/\/example\.com\/embed["'][^>]*title=["']Demo Embed["'][^>]*><\/iframe>/i);
  assertNoTodo(html);
});
"""
),
  ("html-meta-seo", "Metadata & SEO Basics",
"""# Metadata & SEO Basics

Edit `index.html`.

Requirements in `<head>`:
1) `<title>EvalForge Web Quest</title>`
2) `<meta name="description" content="EvalForge web training quest.">`
3) `<link rel="canonical" href="https://example.com/quest">`
4) `<meta property="og:title" content="EvalForge">`
""",
"<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"></head><body>TODO</body></html>\n",
"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\">\n  <title>EvalForge Web Quest</title>\n  <meta name=\"description\" content=\"EvalForge web training quest.\" />\n  <link rel=\"canonical\" href=\"https://example.com/quest\" />\n  <meta property=\"og:title\" content=\"EvalForge\" />\n</head>\n<body>\n  <main>SEO Ready</main>\n</body>\n</html>\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, assertMatches, assertTagText } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("meta + seo", () => {
  const html = normLF(readText(WS, "index.html"));
  assertTagText(html, "title", "EvalForge Web Quest");
  assertMatches(html, /<meta\s+name=["']description["']\s+content=["']EvalForge web training quest\.[\"']\s*\/?>/i);
  assertMatches(html, /<link\s+rel=["']canonical["']\s+href=["']https:\/\/example\.com\/quest["']\s*\/?>/i);
  assertMatches(html, /<meta\s+property=["']og:title["']\s+content=["']EvalForge["']\s*\/?>/i);
  assertNoTodo(html);
});
"""
),
  ("html-debug-validate", "Debug & Validate HTML",
"""# Debug & Validate HTML

Edit `index.html`.

Fix these common issues:
1) Must include `<meta charset="utf-8">`
2) `<ul data-testid="menu">` must have 2 `<li>` items: Home, About
3) `<a data-testid="home-link" href="/home">Home</a>` must be a valid link
4) No invalid nesting like `<p><div>...`
""",
"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <title>Broken</title>\n</head>\n<body>\n  <p><div>Bad nesting</div></p>\n  <ul data-testid=\"menu\">\n    <li>Home\n    <li>About\n  </ul>\n  <a data-testid=\"home-link\">Home</a>\n</body>\n</html>\n",
"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\">\n  <title>Debugged</title>\n</head>\n<body>\n  <div>Good nesting</div>\n  <ul data-testid=\"menu\">\n    <li>Home</li>\n    <li>About</li>\n  </ul>\n  <a data-testid=\"home-link\" href=\"/home\">Home</a>\n</body>\n</html>\n",
r"""
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertMatches, assertNoTodo } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("debug + validate", () => {
  const html = normLF(readText(WS, "index.html"));
  assertMatches(html, /<meta\s+charset=["']utf-8["']\s*\/?>/i);
  assert.ok(!/<p>\s*<div>/i.test(html), "must not nest div inside p");

  const m = html.match(/<ul\b[^>]*data-testid=["']menu["'][^>]*>([\s\S]*?)<\/ul>/i);
  assert.ok(m, "menu ul");
  const li = (m[1].match(/<li\b[^>]*>[\s\S]*?<\/li>/gi) || []).map(s => s.replace(/<[^>]+>/g,"").trim());
  assert.deepEqual(li, ["Home","About"]);

  assertMatches(html, /<a\b[^>]*data-testid=["']home-link["'][^>]*href=["']\/home["'][^>]*>\s*Home\s*<\/a>/i);
  assertNoTodo(html);
});
"""
),
]

# CSS specs: (slug, title, readme, starter_style, solution_style, test_js)
CSS_SPECS = [
  ("css-ignition","CSS Ignition: Your First Styles",
"""# CSS Ignition: Your First Styles

Edit `style.css`.

Requirements:
1) body:
   - background: #111
   - color: #eee
   - font-family: system-ui
2) .container:
   - max-width: 800px
   - margin: 0 auto
3) h1:
   - font-size: 2rem
""",
"/* TODO: Implement styles */\nbody {\n  background: #000;\n}\n",
"body {\n  background: #111;\n  color: #eee;\n  font-family: system-ui;\n}\n\n.container {\n  max-width: 800px;\n  margin: 0 auto;\n}\n\nh1 {\n  font-size: 2rem;\n}\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("css ignition", () => {
  const css = normLF(readText(WS, "style.css"));
  const body = cssFindBlock(css, "body");
  cssAssertDecl(body, "background", "#111");
  cssAssertDecl(body, "color", "#eee");
  cssAssertDecl(body, "font-family", "system-ui");

  const c = cssFindBlock(css, ".container");
  cssAssertDecl(c, "max-width", "800px");
  cssAssertDecl(c, "margin", "0 auto");

  const h1 = cssFindBlock(css, "h1");
  cssAssertDecl(h1, "font-size", "2rem");

  assertNoTodo(css);
});
"""
),
  ("css-selectors-specificity","Selectors & Specificity",
"""# Selectors & Specificity

Edit `style.css`.

Requirements:
1) `.btn` sets padding: 10px
2) `.btn.primary` sets background: #4f46e5
3) `#cta.btn.primary` sets border: 2px solid #fff
""",
"/* TODO */\n.btn { }\n",
".btn { padding: 10px; }\n.btn.primary { background: #4f46e5; }\n#cta.btn.primary { border: 2px solid #fff; }\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("selectors + specificity", () => {
  const css = normLF(readText(WS, "style.css"));
  cssAssertDecl(cssFindBlock(css, ".btn"), "padding", "10px");
  cssAssertDecl(cssFindBlock(css, ".btn.primary"), "background", "#4f46e5");
  cssAssertDecl(cssFindBlock(css, "#cta.btn.primary"), "border", "2px solid #fff");
  assertNoTodo(css);
});
"""
),
  ("css-cascade-inheritance","Cascade & Inheritance",
"""# Cascade & Inheritance

Edit `style.css`.

Requirements:
1) body sets color: #222
2) p sets color: inherit
3) .muted sets color: #666
""",
"/* TODO */\n",
"body { color: #222; }\np { color: inherit; }\n.muted { color: #666; }\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("cascade + inheritance", () => {
  const css = normLF(readText(WS, "style.css"));
  cssAssertDecl(cssFindBlock(css, "body"), "color", "#222");
  cssAssertDecl(cssFindBlock(css, "p"), "color", "inherit");
  cssAssertDecl(cssFindBlock(css, ".muted"), "color", "#666");
  assertNoTodo(css);
});
"""
),
  ("css-box-model","The Box Model",
"""# The Box Model

Edit `style.css`.

Requirements for `.box`:
- width: 200px
- padding: 16px
- border: 2px solid #000
- margin: 12px
- box-sizing: border-box
""",
"/* TODO */\n.box {}\n",
".box {\n  width: 200px;\n  padding: 16px;\n  border: 2px solid #000;\n  margin: 12px;\n  box-sizing: border-box;\n}\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("box model", () => {
  const css = normLF(readText(WS, "style.css"));
  const b = cssFindBlock(css, ".box");
  cssAssertDecl(b, "width", "200px");
  cssAssertDecl(b, "padding", "16px");
  cssAssertDecl(b, "border", "2px solid #000");
  cssAssertDecl(b, "margin", "12px");
  cssAssertDecl(b, "box-sizing", "border-box");
  assertNoTodo(css);
});
"""
),
  ("css-units-typography","Units & Typography",
"""# Units & Typography

Edit `style.css`.

Requirements:
- html font-size: 16px
- h1 font-size: 2rem
- p line-height: 1.5
- .caption font-size: 0.875rem
""",
"/* TODO */\n",
"html { font-size: 16px; }\nh1 { font-size: 2rem; }\np { line-height: 1.5; }\n.caption { font-size: 0.875rem; }\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("units + typography", () => {
  const css = normLF(readText(WS, "style.css"));
  cssAssertDecl(cssFindBlock(css, "html"), "font-size", "16px");
  cssAssertDecl(cssFindBlock(css, "h1"), "font-size", "2rem");
  cssAssertDecl(cssFindBlock(css, "p"), "line-height", "1.5");
  cssAssertDecl(cssFindBlock(css, ".caption"), "font-size", "0.875rem");
  assertNoTodo(css);
});
"""
),
  ("css-colors-backgrounds","Colors & Backgrounds",
"""# Colors & Backgrounds

Edit `style.css`.

Requirements:
- .hero has background: linear-gradient(...)
- .hero has color: #fff
- body has background-color: #0b1020
""",
"/* TODO */\n",
"body { background-color: #0b1020; }\n.hero { background: linear-gradient(90deg, #4f46e5, #06b6d4); color: #fff; }\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("colors + backgrounds", () => {
  const css = normLF(readText(WS, "style.css"));
  cssAssertDecl(cssFindBlock(css, "body"), "background-color", "#0b1020");

  const heroBlock = cssFindBlock(css, ".hero");
  assertMatches(heroBlock, /background\s*:\s*linear-gradient/i, "hero must use linear-gradient");
  cssAssertDecl(heroBlock, "color", "#fff");

  assertNoTodo(css);
});
"""
),
  ("css-flexbox","Flexbox Layout",
"""# Flexbox Layout

Edit `style.css`.

Requirements:
- .row display: flex
- .row justify-content: space-between
- .row align-items: center
- .row gap: 12px
""",
"/* TODO */\n",
".row { display: flex; justify-content: space-between; align-items: center; gap: 12px; }\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("flexbox", () => {
  const css = normLF(readText(WS, "style.css"));
  const row = cssFindBlock(css, ".row");
  cssAssertDecl(row, "display", "flex");
  cssAssertDecl(row, "justify-content", "space-between");
  cssAssertDecl(row, "align-items", "center");
  cssAssertDecl(row, "gap", "12px");
  assertNoTodo(css);
});
"""
),
  ("css-grid","Grid Layout",
"""# Grid Layout

Edit `style.css`.

Requirements:
- .grid display: grid
- .grid grid-template-columns: repeat(3, 1fr)
- .grid gap: 12px
""",
"/* TODO */\n",
".grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("grid", () => {
  const css = normLF(readText(WS, "style.css"));
  const grid = cssFindBlock(css, ".grid");
  cssAssertDecl(grid, "display", "grid");
  cssAssertDecl(grid, "grid-template-columns", "repeat(3, 1fr)");
  cssAssertDecl(grid, "gap", "12px");
  assertNoTodo(css);
});
"""
),
  ("css-responsive-media","Responsive Design & Media Queries",
"""# Responsive Design & Media Queries

Edit `style.css`.

Requirements:
1) Base:
   - .row display: flex
   - .grid has 3 columns
2) In `@media (max-width: 600px)`:
   - .row flex-direction: column
   - .grid grid-template-columns: 1fr
""",
"/* TODO */\n",
".row { display: flex; }\n.grid { display: grid; grid-template-columns: repeat(3, 1fr); }\n\n@media (max-width: 600px) {\n  .row { flex-direction: column; }\n  .grid { grid-template-columns: 1fr; }\n}\n",
r"""
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl, assertMatches } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("responsive media queries", () => {
  const css = normLF(readText(WS, "style.css"));
  cssAssertDecl(cssFindBlock(css, ".row"), "display", "flex");
  cssAssertDecl(cssFindBlock(css, ".grid"), "grid-template-columns", "repeat(3, 1fr)");

  assertMatches(css, /@media\s*\(\s*max-width\s*:\s*600px\s*\)\s*\{([\s\S]*)\}\s*$/m, "media query required");

  const mq = css.match(/@media\s*\(\s*max-width\s*:\s*600px\s*\)\s*\{([\s\S]*)\}\s*$/m);
  assert.ok(mq, "media query block");
  assertMatches(mq[1], /\.row\s*\{[\s\S]*flex-direction\s*:\s*column/i, "row becomes column");
  assertMatches(mq[1], /\.grid\s*\{[\s\S]*grid-template-columns\s*:\s*1fr/i, "grid becomes 1fr");

  assertNoTodo(css);
});
"""
),
  ("css-position-zindex","Positioning & Z-Index",
"""# Positioning & Z-Index

Edit `style.css`.

Requirements:
- .modal: position fixed; inset 0; z-index 1000
- .tooltip: position absolute; z-index 1100
- .fab: position fixed; right 16px; bottom 16px
""",
"/* TODO */\n",
".modal { position: fixed; inset: 0; z-index: 1000; }\n.tooltip { position: absolute; z-index: 1100; }\n.fab { position: fixed; right: 16px; bottom: 16px; }\n",
r"""
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readText, normLF, assertNoTodo, cssFindBlock, cssAssertDecl } from "../../../_shared/web_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("position + z-index", () => {
  const css = normLF(readText(WS, "style.css"));
  const modal = cssFindBlock(css, ".modal");
  cssAssertDecl(modal, "position", "fixed");
  cssAssertDecl(modal, "inset", "0");
  cssAssertDecl(modal, "z-index", "1000");

  const tip = cssFindBlock(css, ".tooltip");
  cssAssertDecl(tip, "position", "absolute");
  cssAssertDecl(tip, "z-index", "1100");

  const fab = cssFindBlock(css, ".fab");
  cssAssertDecl(fab, "position", "fixed");
  cssAssertDecl(fab, "right", "16px");
  cssAssertDecl(fab, "bottom", "16px");

  assertNoTodo(css);
});
"""
),
]

def write_file(p: Path, content: str, force: bool):
  p.parent.mkdir(parents=True, exist_ok=True)
  if p.exists() and not force:
    return
  p.write_text(content.replace("\r\n", "\n"), encoding="utf-8")

def scaffold_one(slug: str, readme: str, workspace_files: dict[str,str], sol_files: dict[str,str], public_test: str, force: bool):
  base = DATA_QUESTS / slug
  ws = base / "workspace"
  pub = base / "grading" / "public"
  sol = base / "grading" / "solutions"

  # Workspace
  write_file(ws / "README.md", readme, force)
  for name, content in workspace_files.items():
    write_file(ws / name, content, force)

  # Solutions
  for name, content in sol_files.items():
    write_file(sol / name, content, force)

  # Public tests
  write_file(pub / f"{slug}.public.test.mjs", public_test, force)

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--force", action="store_true", help="overwrite existing files")
  args = ap.parse_args()

  for slug, title, readme, starter_html, solution_html, test_js in HTML_SPECS:
    scaffold_one(
      slug=slug,
      readme=readme,
      workspace_files={"index.html": starter_html},
      sol_files={"index.html": solution_html},
      public_test=test_js,
      force=args.force
    )

  for slug, title, readme, starter_css, solution_css, test_js in CSS_SPECS:
    # include a simple index.html so learners can open it locally if they want
    scaffold_one(
      slug=slug,
      readme=readme,
      workspace_files={
        "index.html": "<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><link rel=\"stylesheet\" href=\"style.css\"><title>CSS Quest</title></head><body><div class=\"container\"><h1>Hello</h1></div></body></html>\n",
        "style.css": starter_css
      },
      sol_files={"style.css": solution_css},
      public_test=test_js,
      force=args.force
    )

  print("EF_WEB_SCAFFOLD_DONE: html=10 css=10 total=20")

if __name__ == "__main__":
  main()
