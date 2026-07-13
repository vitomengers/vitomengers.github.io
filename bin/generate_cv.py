#!/usr/bin/env python3
"""Generate a LaTeX CV for Vito Mengers from the repository's own data.

Sources
-------
* ``_data/cv.yml``        -- Education, Experience, Volunteer, Awards, Academic Service
* ``_bibliography/papers.bib`` -- Publications (grouped by ``papertype``)
* ``_teachings/*.md``     -- Teaching & supervision
* ``_talks/*.md``         -- Talks & posters
* ``_outreach/*.md``      -- Public engagement / outreach

The script writes a self-contained ``.tex`` file (compilable with plain
``pdflatex``/``latexmk``) to ``assets/cv/vito_mengers_cv.tex``. Compilation is
done separately (locally via ``latexmk`` or in CI via a TeXLive action).

Only the standard library plus PyYAML is required, so the same script runs
locally and in GitHub Actions without a heavy dependency install.
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import sys

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Order in which publication categories appear, with their section headings.
PUBTYPE_ORDER = [
    ("journal", "Journal Articles"),
    ("conference", "Conference Papers"),
    ("workshop_or_abstract", "Workshop Papers \\& Extended Abstracts"),
    ("preprint", "Preprints \\& Under Review"),  # non-peer-reviewed, listed last
]

OWN_LAST_NAME = "Mengers"


# --------------------------------------------------------------------------- #
# LaTeX text helpers
# --------------------------------------------------------------------------- #
def tex_escape_text(text: str) -> str:
    """Escape LaTeX special characters in a plain-text fragment."""
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return re.sub(r"[\\&%$#_{}~^]", lambda m: repl[m.group()], text)


def _escape_url(url: str) -> str:
    return url.replace("\\", "").replace("%", r"\%").replace("#", r"\#")


def html_to_latex(raw, markdown: bool = False) -> str:
    """Convert the limited HTML/Markdown used across the repo into LaTeX.

    Handles ``<a href>``, ``<em>/<i>``, ``<u>``, ``<b>/<strong>``, ``<sup>``,
    ``<br>`` and strips ``<span>``. When ``markdown`` is true, ``**bold**`` and
    ``*italic*`` are also converted (kept off for BibTeX author fields, whose
    ``*`` markers denote equal contribution).
    """
    if raw is None:
        return ""
    s = str(raw)

    # Normalise unicode punctuation that T1 fonts may not carry cleanly.
    s = (
        s.replace("∗", "*")   # ∗ -> *
        .replace("–", "--")   # – en dash
        .replace("—", "---")  # — em dash
        .replace("“", "``")   # “
        .replace("”", "''")   # ”
        .replace("‘", "`")    # ‘
        .replace("’", "'")    # ’
        .replace(" ", " ")    # nbsp
    )
    # Emoji shortcodes such as :trophy:
    s = re.sub(r":[a-z0-9_+-]+:", "", s)

    if markdown:
        s = re.sub(r"\*\*(.+?)\*\*", lambda m: "<b>" + m.group(1) + "</b>", s)
        s = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)",
                   lambda m: "<em>" + m.group(1) + "</em>", s)

    out = []
    for part in re.split(r"(<[^>]+>)", s):
        if not part:
            continue
        if part.startswith("<") and part.endswith(">"):
            tag = part[1:-1].strip()
            low = tag.lower()
            if low.startswith("a "):
                m = re.search(r"href\s*=\s*['\"]([^'\"]+)['\"]", tag, re.I)
                url = _escape_url(m.group(1)) if m else ""
                out.append(r"\href{" + url + "}{")
            elif low == "/a":
                out.append("}")
            elif low in ("em", "i"):
                out.append(r"\emph{")
            elif low in ("/em", "/i"):
                out.append("}")
            elif low == "u":
                out.append(r"\underline{")
            elif low == "/u":
                out.append("}")
            elif low in ("b", "strong"):
                out.append(r"\textbf{")
            elif low in ("/b", "/strong"):
                out.append("}")
            elif low == "sup":
                out.append(r"\textsuperscript{")
            elif low == "/sup":
                out.append("}")
            elif low.startswith("br"):
                out.append(r"\newline ")
            # <span ...>, </span> and anything unknown are dropped.
        else:
            out.append(tex_escape_text(part))
    # Collapse whitespace but keep explicit \newline breaks.
    result = "".join(out)
    result = re.sub(r"[ \t]+", " ", result).strip()
    return result


# --------------------------------------------------------------------------- #
# BibTeX parsing
# --------------------------------------------------------------------------- #
def _strip_braces(value: str) -> str:
    return value.replace("{", "").replace("}", "").strip()


def parse_bib(text: str):
    """Return a list of entry dicts. Resolves @string abbreviations."""
    text = re.sub(r"^\s*---.*?---\s*", "", text, count=1, flags=re.S)
    strings: dict[str, str] = {}
    entries = []
    i, n = 0, len(text)
    while True:
        at = text.find("@", i)
        if at == -1:
            break
        brace = text.find("{", at)
        if brace == -1:
            break
        etype = text[at + 1:brace].strip().lower()
        depth, k = 0, brace
        while k < n:
            c = text[k]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        body = text[brace + 1:k]
        i = k + 1

        if etype == "string":
            m = re.match(r"\s*(\w+)\s*=\s*", body)
            if m:
                strings[m.group(1).lower()] = _strip_braces(body[m.end():])
            continue
        if etype in ("comment", "preamble"):
            continue

        comma = body.find(",")
        key = body[:comma].strip()
        fields = _parse_fields(body[comma + 1:], strings)
        fields["__type__"] = etype
        fields["__key__"] = key
        entries.append(fields)
    return entries


def _parse_fields(s: str, strings: dict) -> dict:
    fields, i, n = {}, 0, len(s)
    while i < n:
        while i < n and s[i] in " \t\r\n,":
            i += 1
        m = re.match(r"([A-Za-z_][\w-]*)\s*=\s*", s[i:])
        if not m:
            break
        name = m.group(1).lower()
        i += m.end()
        if i >= n:
            break
        if s[i] == "{":
            depth, k = 0, i
            while k < n:
                if s[k] == "{":
                    depth += 1
                elif s[k] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                k += 1
            fields[name] = s[i + 1:k]
            i = k + 1
        elif s[i] == '"':
            k = i + 1
            while k < n and s[k] != '"':
                k += 1
            fields[name] = s[i + 1:k]
            i = k + 1
        else:
            m2 = re.match(r"[^,]+", s[i:])
            token = m2.group(0).strip()
            fields[name] = strings.get(token.lower(), token)
            i += m2.end()
    return fields


def format_authors(raw: str, legend_state: list) -> str:
    """Turn a BibTeX ``author`` field into ``V. Mengers, A. Battaje, ...``.

    A single trailing ``*`` on a surname marks equal contribution and is kept
    as a superscript; ``**`` marks equal supervision and is dropped. ``legend_state``
    is a one-element list used to attach the explanatory footnote only once.
    """
    authors = []
    for chunk in re.split(r"\s+and\s+", raw.strip()):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "," in chunk:
            last, first = chunk.split(",", 1)
        else:
            bits = chunk.rsplit(" ", 1)
            first, last = (bits[0], bits[1]) if len(bits) == 2 else ("", chunk)
        last = last.strip()
        m = re.search(r"[*∗†‡§]+$", last)
        markers = m.group(0).replace("∗", "*") if m else ""
        last = (last[: m.start()] if m else last).strip()
        equal_contrib = markers == "*"  # exactly one star; ** = equal supervision (dropped)

        initials = " ".join(
            f"{p[0]}." for p in re.split(r"[\s-]+", first.strip()) if p
        )
        name = html_to_latex(f"{initials} {last}".strip())
        if last == OWN_LAST_NAME:
            name = r"\textbf{" + name + "}"
        if equal_contrib:
            if not legend_state[0]:
                # \fnsymbol makes the (single) footnote's marker a "*", matching
                # the manual superscripts on the other equal-contribution authors.
                name += r"\footnote{Equal contribution.}"
                legend_state[0] = True
            else:
                name += r"\textsuperscript{*}"
        authors.append(name)
    if len(authors) > 2:
        return ", ".join(authors[:-1]) + ", and " + authors[-1]
    if len(authors) == 2:
        return authors[0] + " and " + authors[1]
    return authors[0] if authors else ""


def render_publications(bib_path: str) -> str:
    with open(bib_path, encoding="utf-8") as fh:
        entries = parse_bib(fh.read())

    buckets: dict[str, list] = {t: [] for t, _ in PUBTYPE_ORDER}
    for e in entries:
        buckets.setdefault(e.get("papertype", "").strip(), []).append(e)

    legend_state = [False]  # flips to True once the equal-contribution footnote is placed
    out = []
    for ptype, heading in PUBTYPE_ORDER:
        items = sorted(
            buckets.get(ptype, []),
            key=lambda e: int(re.sub(r"\D", "", e.get("year", "0")) or 0),
            reverse=True,
        )
        if not items:
            continue
        out.append("\\section{%s}" % heading)
        out.append(r"\begin{cvlist}")
        for e in items:
            authors = format_authors(e.get("author", ""), legend_state)
            title = html_to_latex(_strip_braces(e.get("title", "")))
            venue = e.get("journal") or e.get("booktitle") or e.get("howpublished") or ""
            venue = html_to_latex(_strip_braces(venue))
            year = _strip_braces(e.get("year", ""))
            line = f"{authors}. \\textit{{{title}}}."
            if venue:
                line += f" {venue},"
            line += f" {year}."
            links = []
            if e.get("pdf"):
                links.append(r"\href{%s}{PDF}" % _escape_url(e["pdf"]))
            if e.get("html"):
                links.append(r"\href{%s}{Project Page}" % _escape_url(e["html"]))
            if links:
                line += r" \, {\small[" + ", ".join(links) + "]}"
            if e.get("award_name"):
                award = html_to_latex(e["award_name"])
                line += r" \, {\small\textcolor{accent}{\textbf{%s}}}" % award
            out.append(r"  \item " + line)
        out.append(r"\end{cvlist}")
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Markdown collection parsing (front matter + body)
# --------------------------------------------------------------------------- #
def read_front_matter(path: str):
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    m = re.match(r"\s*---\s*\n(.*?)\n---\s*\n?(.*)", content, flags=re.S)
    if not m:
        return {}, content.strip()
    front = yaml.safe_load(m.group(1)) or {}
    return front, m.group(2).strip()


def _collection(dirname: str):
    path = os.path.join(REPO, dirname)
    items = []
    if not os.path.isdir(path):
        return items
    for fn in sorted(os.listdir(path)):
        if fn.endswith(".md"):
            front, body = read_front_matter(os.path.join(path, fn))
            items.append((front, body))
    return items


def _year_of(front: dict) -> int:
    if front.get("year"):
        return int(re.sub(r"\D", "", str(front["year"])) or 0)
    if front.get("date"):
        return int(str(front["date"])[:4] or 0)
    return 0


def cv_entry(primary: str, secondary: str, date: str, body: str = "") -> str:
    """Render a single CV block.

    The whole entry lives in a left minipage with the date/location in a parallel
    right minipage, so title, subtitle and body flow with normal leading (no
    overlap when the title wraps) and never run underneath the date column.
    ``\\exhyphenpenalty`` keeps hyphenated proper nouns from splitting across lines.
    """
    left = [r"\begin{minipage}[t]{0.73\linewidth}\raggedright\exhyphenpenalty=10000\relax",
            r"\textbf{%s}\par" % primary]
    if secondary:
        left.append(r"\vspace{0.15em}{\small\itshape %s}\par" % secondary)
    if body:
        left.append(r"\vspace{0.2em}" + body)
    left.append(r"\end{minipage}")

    return (
        r"\noindent" + "\n"
        + "\n".join(left) + r"\hfill" + "\n"
        + r"\begin{minipage}[t]{0.25\linewidth}\raggedleft{\small\textcolor{black!55}{%s}}\end{minipage}" % (date or "")
        + "\n" + r"\par\vspace{0.55em}" + "\n"
    )


def _thesis_kind(title: str) -> str:
    low = title.lower()
    if "bachelor" in low:
        return "Bachelor's Thesis"
    if "phd" in low or "doctoral" in low:
        return "PhD Thesis"
    return "Master's Thesis"


def render_teaching() -> str:
    items = sorted(_collection("_teachings"), key=lambda it: _year_of(it[0]), reverse=True)
    # Thesis supervision entries carry an `instructor` (the student); course
    # teaching entries do not.
    supervision = [it for it in items if it[0].get("instructor")]
    courses = [it for it in items if not it[0].get("instructor")]

    out = []
    if supervision:
        out.append(r"\section{Student Supervision}")
        for front, _ in supervision:
            student = html_to_latex(front.get("instructor", ""))
            kind = _thesis_kind(front.get("title", ""))
            primary = r"%s \, {\normalfont(%s)}" % (student, kind)
            desc = html_to_latex(front.get("description", ""), markdown=True)
            out.append(cv_entry(primary, desc, str(front.get("year", "")).strip()))
    if courses:
        out.append(r"\section{Teaching}")
        for front, _ in courses:
            title = html_to_latex(front.get("title", ""), markdown=True)
            desc = html_to_latex(front.get("description", ""), markdown=True)
            out.append(cv_entry(title, desc, str(front.get("year", "")).strip()))
    return "\n".join(out)


def render_talks() -> str:
    items = sorted(
        _collection("_talks"),
        key=lambda it: str(it[0].get("date", it[0].get("year", ""))),
        reverse=True,
    )
    if not items:
        return ""
    out = [r"\section{Talks \& Posters}"]
    out.append(r"\begin{cvlist}")
    for front, body in items:
        text = html_to_latex(body.replace("<br>", " — ").replace("<br/>", " — "),
                             markdown=True)
        year = str(front.get("year", "")).strip()
        # Inline (not \hfill) year avoids it wrapping onto its own line when the
        # talk description spans multiple lines.
        out.append(r"  \item %s \, {\small\textcolor{black!55}{(%s)}}" % (text, year))
    out.append(r"\end{cvlist}")
    return "\n".join(out)


def render_outreach() -> str:
    items = sorted(_collection("_outreach"), key=lambda it: _year_of(it[0]), reverse=True)
    if not items:
        return ""
    out = [r"\section{Outreach \& Public Engagement}"]
    for front, _ in items:
        title = html_to_latex(front.get("title", ""), markdown=True)
        desc = html_to_latex(front.get("description", ""), markdown=True)
        out.append(cv_entry(title, desc, str(front.get("year", "")).strip()))
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# cv.yml (hand-written) sections
# --------------------------------------------------------------------------- #
def _dates(item: dict) -> str:
    if item.get("date"):
        return str(item["date"]).strip()
    start = str(item.get("start_date", "")).strip()
    end = str(item.get("end_date", "")).strip()
    if start and end:
        return f"{start}--{end}"
    if start and "end_date" in item:
        return f"{start}--present"
    return start or end


def render_yaml_section(name: str, items: list) -> str:
    out = [r"\section{%s}" % html_to_latex(name)]
    for item in items:
        date = _dates(item)
        location = html_to_latex(item.get("location", ""))

        if "institution" in item:
            primary = html_to_latex(item["institution"])
            secondary = " -- ".join(
                p for p in (html_to_latex(item.get("studyType", "")),
                            html_to_latex(item.get("area", ""))) if p
            )
        elif name.lower().startswith("award") or ("awarder" in item):
            primary = html_to_latex(item.get("title", ""))
            secondary = html_to_latex(item.get("awarder", ""))
        elif name.lower().startswith("academic") or name.lower().endswith("service"):
            primary = html_to_latex(item.get("position", item.get("company", "")))
            secondary = html_to_latex(item.get("company", "") if item.get("position") else "")
        else:  # Experience, Volunteer, ...
            primary = html_to_latex(item.get("company", item.get("position", "")))
            secondary = html_to_latex(item.get("position", "") if item.get("company") else "")

        if location:
            date = f"{location} \\; {date}" if date else location

        body = ""
        if item.get("summary"):
            body = r"{\small %s}" % html_to_latex(item["summary"])
        elif item.get("highlights"):
            bullets = "".join(
                r"  \item %s" % html_to_latex(h) + "\n" for h in item["highlights"]
            )
            body = (r"\begin{itemize}[leftmargin=1.3em,itemsep=1pt,parsep=0pt,topsep=1pt]"
                    "\n" + bullets + r"\end{itemize}")
        out.append(cv_entry(primary, secondary, date, body))
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Header / contact
# --------------------------------------------------------------------------- #
def build_header(cv: dict) -> str:
    name = html_to_latex(cv.get("name", "Vito Mengers"))
    label = html_to_latex(cv.get("label", ""))

    contacts = []
    email = cv.get("email")
    if email:
        contacts.append(r"\href{mailto:%s}{%s}" % (email, tex_escape_text(email)))
    if cv.get("location"):
        contacts.append(html_to_latex(cv["location"]))

    # Homepage + Google Scholar + LinkedIn from _config.yml / _data/socials.yml
    site_url = _config_value("url")
    if site_url:
        contacts.append(r"\href{%s}{%s}" % (site_url, tex_escape_text(re.sub(r"https?://", "", site_url))))
    socials = _load_yaml(os.path.join(REPO, "_data", "socials.yml")) or {}
    if socials.get("scholar_userid"):
        contacts.append(r"\href{https://scholar.google.com/citations?user=%s}{Google Scholar}"
                        % socials["scholar_userid"])
    if socials.get("linkedin_username"):
        contacts.append(r"\href{https://www.linkedin.com/in/%s}{LinkedIn}"
                        % socials["linkedin_username"])

    sep = r" \; \textbullet\; "
    header = [
        r"\begin{center}",
        r"  {\Huge\bfseries\color{accent} %s}\\[0.35em]" % name,
    ]
    if label:
        header.append(r"  {\large %s}\\[0.5em]" % label)
    header.append(r"  {\small %s}" % sep.join(contacts))
    header.append(r"\end{center}")
    header.append(r"\vspace{0.4em}")
    return "\n".join(header)


def render_summary(text: str) -> str:
    """Render the top-of-CV research summary (blank-line-separated paragraphs)."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", str(text).strip()) if p.strip()]
    if not paragraphs:
        return ""
    out = [r"\section{Research}"]
    for para in paragraphs:
        out.append(r"{\small %s}\par\smallskip" % html_to_latex(para, markdown=True))
    return "\n".join(out)


def _load_yaml(path: str):
    try:
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except (OSError, yaml.YAMLError):
        return None


def _config_value(key: str):
    """Cheap single-key lookup in _config.yml (avoids parsing the whole file)."""
    try:
        with open(os.path.join(REPO, "_config.yml"), encoding="utf-8") as fh:
            for line in fh:
                m = re.match(rf"{key}\s*:\s*(.+)", line)
                if m:
                    return m.group(1).strip().strip('"').strip("'") or None
    except OSError:
        pass
    return None


# --------------------------------------------------------------------------- #
# Document assembly
# --------------------------------------------------------------------------- #
PREAMBLE = r"""\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[margin=1.7cm,top=1.4cm,bottom=1.6cm]{geometry}
\usepackage{lmodern}
\usepackage[dvipsnames]{xcolor}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}

\definecolor{accent}{HTML}{006400}
\hypersetup{colorlinks=true,urlcolor=accent,linkcolor=accent,
  pdftitle={Vito Mengers -- Curriculum Vitae},pdfauthor={Vito Mengers}}

\setlength{\parindent}{0pt}
\linespread{1.06}
\renewcommand{\thefootnote}{\fnsymbol{footnote}}  % footnote marker "*" for equal contribution

% Footer on every page: make clear this CV is auto-generated from the website.
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancyfoot[C]{\footnotesize\color{black!45}@@FOOTER@@}

\titleformat{\section}{\normalsize\bfseries\color{accent}\scshape}{}{0em}{}%
  [{\color{accent!70!black}\titlerule[0.7pt]}]
\titlespacing*{\section}{0pt}{1.3em}{0.6em}

% Shared list style for publications, talks, etc. -- roomy item spacing.
\newenvironment{cvlist}
  {\begin{itemize}[leftmargin=1.3em,itemsep=6pt,parsep=1pt,topsep=4pt]}
  {\end{itemize}}

"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate Vito Mengers' LaTeX CV.")
    ap.add_argument("--out", default=os.path.join(REPO, "assets", "cv", "vito_mengers_cv.tex"))
    args = ap.parse_args()

    cv_data = _load_yaml(os.path.join(REPO, "_data", "cv.yml")) or {}
    cv = cv_data.get("cv", {})
    sections = cv.get("sections", {}) or {}

    # Footer disclosing that this document is auto-generated from the website.
    gen_date = datetime.date.today().strftime("%-d %B %Y")
    footer = (
        r"This CV was automatically generated from the content of "
        r"\href{https://vitomengers.github.io/cv/}{vitomengers.github.io} "
        r"on " + gen_date + r"."
    )
    preamble = PREAMBLE.replace("@@FOOTER@@", footer)

    parts = [preamble, r"\begin{document}", build_header(cv)]

    # Research summary up top, so a committee sees the framing first.
    if cv.get("summary"):
        parts.append(render_summary(cv["summary"]))

    # Curated section order: for a postdoc CV, publications come right after
    # Education and outrank Experience / Awards / Service.
    def yaml_section(name):
        if sections.get(name):
            parts.append(render_yaml_section(name, sections[name]))

    yaml_section("Education")
    parts.append(render_publications(os.path.join(REPO, "_bibliography", "papers.bib")))
    # Experience and Volunteer are merged into one "Experience" section (the web
    # page's cv.liquid does the same), so a standing membership isn't shown under
    # a stray "Volunteer" heading.
    experience = (sections.get("Experience") or []) + (sections.get("Volunteer") or [])
    if experience:
        parts.append(render_yaml_section("Experience", experience))
    yaml_section("Awards and Scholarships")
    yaml_section("Academic Service")

    # Any other hand-written cv.yml sections we didn't explicitly place.
    placed = {"Education", "Experience", "Volunteer", "Awards and Scholarships", "Academic Service"}
    for name, items in sections.items():
        if name not in placed and items:
            parts.append(render_yaml_section(name, items))

    # Generated sections from the rest of the repository.
    parts.append(render_teaching())
    parts.append(render_talks())
    parts.append(render_outreach())

    parts.append(r"\end{document}")
    tex = "\n\n".join(p for p in parts if p) + "\n"

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(tex)
    print(f"Wrote {args.out} ({len(tex)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
