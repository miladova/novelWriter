#!/usr/bin/env python3
"""Typeset A HOUSE OF GRACES to a print-style 6x9 PDF."""

import glob
import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, NextPageTemplate, PageBreak,
    PageTemplate, Paragraph, Spacer,
)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
FONTDIR = os.path.join(HERE, "fonts")
CHAPDIR = os.path.join(HERE, "chapters")
OUT = os.path.join(HERE, "out", "A House of Graces.pdf")

TITLE = "A House of Graces"
SUBTITLE = "A Novel of Rome"
YEAR = "AD 111\u2013112"

PAGE_W, PAGE_H = 6.0 * inch, 9.0 * inch
M_TOP = 0.78 * inch
M_BOT = 0.78 * inch
M_SIDE = 0.76 * inch

INK = colors.HexColor("#191919")
FADE = colors.HexColor("#5c5c5c")

CH_WORDS = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
            "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen",
            "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen",
            "Twenty", "Twenty-one", "Twenty-two", "Twenty-three",
            "Twenty-four", "Twenty-five"]


# --------------------------------------------------------------- fonts

def register_fonts():
    faces = {
        "Garamond": "EBGaramond-Regular.ttf",
        "Garamond-It": "EBGaramond-Italic.ttf",
        "Garamond-Bd": "EBGaramond-Bold.ttf",
        "Garamond-BdIt": "EBGaramond-BoldItalic.ttf",
        "Garamond-Med": "EBGaramond-Medium.ttf",
    }
    for name, fn in faces.items():
        path = os.path.join(FONTDIR, fn)
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily(
        "Garamond", normal="Garamond", bold="Garamond-Bd",
        italic="Garamond-It", boldItalic="Garamond-BdIt")


def tw(text, font, size, tracking=0.0):
    return (pdfmetrics.stringWidth(text, font, size)
            + tracking * max(0, len(text) - 1))


def draw_tracked(c, x, y, text, font, size, tracking=0.0):
    t = c.beginText(x, y)
    t.setFont(font, size)
    if tracking:
        t.setCharSpace(tracking)
    t.textOut(text)
    c.drawText(t)


# --------------------------------------------------------------- flowables

def diamond(c, cx, cy, s):
    p = c.beginPath()
    p.moveTo(cx, cy + s)
    p.lineTo(cx + s, cy)
    p.lineTo(cx, cy - s)
    p.lineTo(cx - s, cy)
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def diamonds_at(c, cx, cy, s=1.8, gap=7.0):
    step = 2 * s + gap
    for i in (-1, 0, 1):
        diamond(c, cx + i * step, cy, s)


class Tracked(Flowable):
    def __init__(self, text, font="Garamond-Med", size=10, tracking=2.4,
                 color=INK, space_before=0, space_after=0):
        Flowable.__init__(self)
        self.text = text.upper()
        self.font, self.size, self.tracking = font, size, tracking
        self.color = color
        self.sb, self.sa = space_before, space_after

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.size + self.sb + self.sa

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(self.color)
        w = tw(self.text, self.font, self.size, self.tracking)
        draw_tracked(c, (self.width - w) / 2.0, self.sa, self.text,
                     self.font, self.size, self.tracking)
        c.restoreState()


class Ornament(Flowable):
    def __init__(self, height=34, size=1.8, gap=7.0, color=FADE, space_before=0):
        Flowable.__init__(self)
        self.h, self.s, self.gap, self.color = height, size, gap, color
        self.sb = space_before

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.h + self.sb

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(self.color)
        diamonds_at(c, self.width / 2.0, self.sb + 6, self.s, self.gap)
        c.restoreState()


class SceneBreak(Flowable):
    def wrap(self, aw, ah):
        self.width = aw
        return aw, 26

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(FADE)
        diamonds_at(c, self.width / 2.0, 12, 1.45, 5.5)
        c.restoreState()


class Rule(Flowable):
    def __init__(self, frac=0.14, thickness=0.4, color=FADE,
                 space_before=0, space_after=0):
        Flowable.__init__(self)
        self.frac, self.t, self.color = frac, thickness, color
        self.sb, self.sa = space_before, space_after

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.t + self.sb + self.sa

    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(self.color)
        c.setLineWidth(self.t)
        w = self.width * self.frac
        c.line((self.width - w) / 2.0, self.sa, (self.width + w) / 2.0, self.sa)
        c.restoreState()


class ChapterHead(Flowable):
    def __init__(self, word, ordinal):
        Flowable.__init__(self)
        self.word, self.ordinal = word, ordinal

    def wrap(self, aw, ah):
        self.width = aw
        return aw, 108

    def draw(self):
        c = self.canv
        w = self.width
        c.saveState()
        label = "C H A P T E R"
        c.setFillColor(FADE)
        draw_tracked(c, (w - tw(label, "Garamond-Med", 8.2)) / 2.0, 88,
                     label, "Garamond-Med", 8.2)
        c.setFillColor(INK)
        word = self.word.upper()
        draw_tracked(c, (w - tw(word, "Garamond-Med", 24, 5.0)) / 2.0, 48,
                     word, "Garamond-Med", 24, 5.0)
        c.setFillColor(FADE)
        diamonds_at(c, w / 2.0, 24, 1.9, 7.5)
        c.restoreState()


class SectionMark(Flowable):
    def __init__(self, name):
        Flowable.__init__(self)
        self.name = name

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        pass


# --------------------------------------------------------------- document

class Book(BaseDocTemplate):
    def __init__(self, filename):
        BaseDocTemplate.__init__(
            self, filename, pagesize=(PAGE_W, PAGE_H),
            leftMargin=M_SIDE, rightMargin=M_SIDE,
            topMargin=M_TOP, bottomMargin=M_BOT,
            allowSplitting=1, title=TITLE,
            author="", subject=SUBTITLE, creator="",
            invariant=0)
        fw = PAGE_W - 2 * M_SIDE
        fh = PAGE_H - M_TOP - M_BOT
        frame = Frame(M_SIDE, M_BOT, fw, fh, id="main",
                      leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="plain", frames=[frame], onPageEnd=self.decorate_plain),
            PageTemplate(id="body", frames=[frame], onPageEnd=self.decorate_body),
        ])
        self.current_chapter = ""
        self.chapter_start_page = None
        self.chapter_starts = {}
        self.body_start = None
        self.section = "front"

    def folio(self):
        if self.body_start is None:
            return None
        return self.page - (self.body_start - 1)

    def decorate_plain(self, c, doc):
        pass

    def decorate_body(self, c, doc):
        n = self.folio()
        c.saveState()
        c.setFillColor(FADE)
        if self.section == "body" and self.chapter_start_page != doc.page:
            label = ("Chapter " + self.current_chapter
                     if doc.page % 2 == 1 else TITLE.upper())
            draw_tracked(c, (PAGE_W - tw(label, "Garamond", 7.2, 1.9)) / 2.0,
                         PAGE_H - M_TOP + 24, label, "Garamond", 7.2, 1.9)
        if n and n > 0:
            s = str(n)
            draw_tracked(c, (PAGE_W - tw(s, "Garamond", 9.0, 0.6)) / 2.0,
                         M_BOT - 32, s, "Garamond", 9.0, 0.6)
        c.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, ChapterHead):
            self.current_chapter = flowable.word
            self.chapter_start_page = self.page
            self.chapter_starts[flowable.ordinal] = self.page
            if self.body_start is None:
                self.body_start = self.page
            key = "ch%02d" % flowable.ordinal
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry("Chapter " + flowable.word,
                                      key, 0, 0)
            self.notify("TOCEntry", (0, "Chapter " + flowable.word,
                                     max(1, self.folio() or 1), key))
        elif isinstance(flowable, SectionMark):
            self.section = flowable.name


# --------------------------------------------------------------- styles

def styles():
    body = ParagraphStyle(
        "body", fontName="Garamond", fontSize=10.6, leading=15.1,
        alignment=TA_JUSTIFY, firstLineIndent=14.5, spaceBefore=0,
        spaceAfter=0, textColor=INK, hyphenationLang="en_GB",
        hyphenationMinWordLength=5, embeddedHyphenation=0,
        allowWidows=0, allowOrphans=0, splitLongWords=1,
        justifyLastLine=0, spaceShrinkage=0.05, endDots=None)
    S = {"body": body}
    S["first"] = ParagraphStyle("first", parent=body, firstLineIndent=0,
                                spaceBefore=7)
    S["title"] = ParagraphStyle("title", fontName="Garamond-Med", fontSize=30,
                                leading=36, alignment=TA_CENTER, textColor=INK)
    S["subtitle"] = ParagraphStyle("subtitle", fontName="Garamond-It",
                                   fontSize=12.5, leading=19,
                                   alignment=TA_CENTER, textColor=FADE)
    S["copy"] = ParagraphStyle("copy", fontName="Garamond", fontSize=8.4,
                               leading=12.2, alignment=TA_CENTER, textColor=FADE)
    S["epigraph"] = ParagraphStyle("epigraph", fontName="Garamond-It",
                                   fontSize=11.5, leading=17,
                                   alignment=TA_CENTER, textColor=INK)
    S["epiattr"] = ParagraphStyle("epiattr", fontName="Garamond", fontSize=8,
                                  leading=12, alignment=TA_CENTER, textColor=FADE)
    S["toc"] = ParagraphStyle("toc", fontName="Garamond", fontSize=9.8,
                              leading=13.2, textColor=INK)
    S["tochead"] = ParagraphStyle("tochead", fontName="Garamond-Med",
                                  fontSize=11.5, leading=18,
                                  alignment=TA_CENTER, textColor=INK)
    S["gloss"] = ParagraphStyle("gloss", fontName="Garamond", fontSize=9.3,
                                leading=12.8, alignment=TA_JUSTIFY,
                                textColor=INK, spaceAfter=3.6,
                                hyphenationLang="en_GB")
    S["note"] = ParagraphStyle("note", parent=body, firstLineIndent=0,
                               spaceAfter=7)
    return S


# --------------------------------------------------------------- text

OPENERS = set("([{\u2014\u2013-\u2018\u201c/ \n\t")


def smarten(s):
    out = []
    prev = ""
    for ch in s:
        if ch == '"':
            out.append("\u201c" if (prev == "" or prev in OPENERS) else "\u201d")
        elif ch == "'":
            out.append("\u2018" if (prev == "" or prev in OPENERS) else "\u2019")
        else:
            out.append(ch)
        prev = ch
    return "".join(out)


def inline(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)
    s = s.replace(" -- ", " \u2014 ").replace("...", "\u2026")
    return smarten(s)


def paragraphs(path):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    out = []
    for block in re.split(r"\n\s*\n", raw):
        block = block.strip()
        if not block:
            continue
        if block.startswith("//"):
            continue
        if block in ("***", "---", "* * *"):
            out.append(None)
        else:
            out.append(" ".join(line.strip() for line in block.splitlines()))
    return out


def load_chapter(path, S):
    story = []
    first = True
    for text in paragraphs(path):
        if text is None:
            story.append(SceneBreak())
            first = True
            continue
        story.append(Paragraph(inline(text), S["first" if first else "body"]))
        first = False
    return story


# --------------------------------------------------------------- front/back

def front_matter(S):
    st = [Spacer(1, 2.0 * inch),
          Tracked(TITLE, size=12.5, tracking=4.2, color=FADE),
          PageBreak(),
          Spacer(1, 1.9 * inch),
          Tracked(TITLE, size=22, tracking=3.0),
          Spacer(1, 12),
          Ornament(height=26, size=2.1, gap=8.5),
          Spacer(1, 2),
          Tracked(SUBTITLE, size=9.2, tracking=3.4, color=FADE),
          Spacer(1, 1.5 * inch),
          Tracked(YEAR, size=8.8, tracking=3.2, color=FADE),
          PageBreak(),
          Spacer(1, 3.5 * inch),
          Paragraph("This is a work of fiction. Names, characters, places and "
                    "incidents are the products of the author\u2019s imagination "
                    "or are used fictitiously. Historical figures who appear in "
                    "these pages are imagined at moments the record does not "
                    "describe.", S["copy"]),
          Spacer(1, 14),
          Rule(frac=0.12, color=FADE, space_before=6, space_after=6),
          Spacer(1, 14),
          Paragraph("<b>MATURE CONTENT \u2014 18+</b>", S["copy"]),
          Spacer(1, 5),
          Paragraph("This novel contains explicit sexual content, sexual "
                    "coercion, slavery, violence, torture and death. "
                    "It is intended for adult readers.", S["copy"]),
          Spacer(1, 26),
          Paragraph("Set in EB Garamond", S["copy"]),
          Paragraph("First edition", S["copy"]),
          PageBreak(),
          Spacer(1, 2.7 * inch),
          Paragraph("\u201cGratia quae tarda est, ingrata est.\u201d", S["epigraph"]),
          Spacer(1, 9),
          Paragraph("A favour that comes late is no favour at all.", S["epiattr"]),
          Spacer(1, 8),
          Tracked("PUBLILIUS SYRUS", size=7.0, tracking=2.4, color=FADE),
          PageBreak(),
          SectionMark("front"),
          Spacer(1, 0.15 * inch),
          Paragraph("CONTENTS", S["tochead"]),
          Ornament(height=28, size=1.6, gap=6.0),
          ]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle(
        "toc1", fontName="Garamond", fontSize=9.8, leading=13.0,
        textColor=INK, leftIndent=6, rightIndent=6, firstLineIndent=0,
        alignment=TA_LEFT)]
    toc.dotsMinLevel = 0
    st += [toc, PageBreak()]
    return st


def load_backmatter(path, S):
    story = []
    first_head = True
    for text in paragraphs(path):
        if text is None:
            story.append(SceneBreak())
            continue
        if text.startswith("% "):
            if not first_head:
                story.append(PageBreak())
            first_head = False
            story.append(Spacer(1, 16))
            story.append(Paragraph(text[2:].upper(), S["tochead"]))
            story.append(Ornament(height=30, size=1.6, gap=6.0))
            continue
        if text.startswith("## "):
            story.append(Spacer(1, 10))
            story.append(Paragraph(inline(text[3:]), S["tochead"]))
            story.append(Spacer(1, 4))
            continue
        if text.startswith("**"):
            story.append(Paragraph(inline(text), S["gloss"]))
        else:
            story.append(Paragraph(inline(text), S["note"]))
    return story


# --------------------------------------------------------------- build

def build(out_path):
    register_fonts()
    S = styles()
    doc = Book(out_path)
    story = front_matter(S)
    story += [SectionMark("body"), NextPageTemplate("body")]

    files = sorted(glob.glob(os.path.join(CHAPDIR, "ch*.md")))
    if len(files) != 25:
        raise SystemExit("expected 25 chapters, found %d" % len(files))
    for i, path in enumerate(files):
        story.append(Spacer(1, 26))
        story.append(ChapterHead(CH_WORDS[i], i + 1))
        story += load_chapter(path, S)
        story.append(PageBreak())

    story += [SectionMark("back"), NextPageTemplate("plain")]
    back = os.path.join(HERE, "backmatter.md")
    if os.path.exists(back):
        story += load_backmatter(back, S)

    doc.multiBuild(story)
    return doc


def wordcount():
    total = 0
    for path in sorted(glob.glob(os.path.join(CHAPDIR, "ch*.md"))):
        n = 0
        for text in paragraphs(path):
            if text:
                n += len(re.findall(r"[A-Za-z0-9\u2019'-]+", text))
        print(os.path.basename(path), n)
        total += n
    print("total", total)


if __name__ == "__main__":
    if "--count" in os.sys.argv:
        wordcount()
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        doc = build(OUT)
        print("pages:", doc.page, "| body starts:", doc.body_start)
        print("written:", OUT)
