#!/usr/bin/env python3
# Copyright 2026 Eluu Labs — Apache-2.0 (see ../LICENSE)
"""
validate_pptx — structural validation of the .pptx that actually shipped.

layout_check.py validates what the builder *intended*: it reads the *.layout.json
the builder emitted. This reads the bytes inside the zip instead, and answers one
question — will PowerPoint open this file, and is every part it points at really
in the package?

Checks (output is grouped under these ids):
  package        the file is a readable zip and no entry fails its CRC
  xml            every .xml / .rels part is well-formed
  content-types  [Content_Types].xml exists and covers every part
  relationships  every non-external rel Target resolves to a part that exists, and
                 every r:id used inside a part is defined in that part's rels
  presentation   ppt/presentation.xml parses; every <p:sldId r:id> resolves to a
                 slide part through ppt/_rels/presentation.xml.rels
  slides         each slide has a rels part, a slideLayout relationship, is listed
                 in <p:sldIdLst>, and defines every r:id its XML references
  media          media/embedding parts no relationship points at (warning only)
  charts         ppt/charts/chart*.xml parses and contains a <c:chart>

Usage:
  python3 validate_pptx.py deck.pptx
  python3 validate_pptx.py deck.pptx --original template.pptx

--original re-runs the same checks on the template and suppresses failures the
template already has, so defects inherited from a template are not blamed on the
generated deck. Exit 0 when clean, 1 on any unsuppressed failure; warnings alone
never fail. Read-only: nothing here writes to either file.
"""
import argparse, posixpath, re, sys, zipfile
import xml.etree.ElementTree as ET
from collections import namedtuple
from urllib.parse import unquote

NS_CT = "http://schemas.openxmlformats.org/package/2006/content-types"
NS_PR = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_R  = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_P  = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_C  = "http://schemas.openxmlformats.org/drawingml/2006/chart"

CHECK_ORDER = ["package", "xml", "content-types", "relationships",
               "presentation", "slides", "media", "charts"]
CT_PART    = "[Content_Types].xml"
PRES_PART  = "ppt/presentation.xml"
PRES_RELS  = "ppt/_rels/presentation.xml.rels"
SLIDE_RE   = re.compile(r"^ppt/slides/slide[^/]*\.xml$")
CHART_RE   = re.compile(r"^ppt/charts/chart[^/]*\.xml$")
RID_RE     = re.compile(r"^rId\d+$")
MEDIA_DIRS = ("ppt/media/", "ppt/embeddings/")

Item = namedtuple("Item", "check sev part detail msg")


class Package:
    """Read-only view of a .pptx zip, with a cache of parsed XML parts."""

    def __init__(self, path):
        self.path = path
        self.zf = zipfile.ZipFile(path)
        self.names = [n for n in self.zf.namelist() if not n.endswith("/")]
        self.parts = set(self.names)
        self._cache = {}

    def xml(self, name):
        """-> (root, error_string). root is None when missing or malformed."""
        if name not in self._cache:
            try:
                self._cache[name] = (ET.fromstring(self.zf.read(name)), None)
            except KeyError:
                self._cache[name] = (None, "part is not in the package")
            except Exception as exc:          # ParseError, BadZipFile, UnicodeError
                self._cache[name] = (None, str(exc))
        return self._cache[name]


class Report:
    def __init__(self):
        self.items, self.notes = [], {}

    def fail(self, check, part, detail, msg):
        self.items.append(Item(check, "FAIL", part, detail, msg))

    def warn(self, check, part, detail, msg):
        self.items.append(Item(check, "WARN", part, detail, msg))

    def note(self, check, text):
        self.notes[check] = text

    def failures(self):
        return [i for i in self.items if i.sev == "FAIL"]


_DIGITS = re.compile(r"\d+")


def signature(item):
    """Identity used to match a deck failure against a template failure.

    Digit runs are collapsed so slide3.xml in the deck matches slide1.xml in the
    template (python-pptx renumbers generated parts). Deliberately loose — see the
    limitations note in the test file.
    """
    norm = lambda s: _DIGITS.sub("#", s or "")
    return (item.check, norm(item.part), norm(item.detail))


# ---- part-name arithmetic (the part that actually catches bugs) --------------

def owner_dir(rels_name):
    """'ppt/slides/_rels/slide1.xml.rels' -> 'ppt/slides'; '_rels/.rels' -> ''."""
    return posixpath.dirname(posixpath.dirname(rels_name))


def owner_part(rels_name):
    """The part a .rels file belongs to; '' for the package-level _rels/.rels."""
    base = posixpath.basename(rels_name)[:-len(".rels")]
    return posixpath.join(owner_dir(rels_name), base) if base else ""


def rels_for(part):
    """The .rels part that carries `part`'s relationships."""
    d, b = posixpath.dirname(part), posixpath.basename(part)
    return posixpath.join(d, "_rels", b + ".rels") if d else posixpath.join("_rels", b + ".rels")


def ext_of(part):
    """OOXML extension of a part name. Note '_rels/.rels' has extension 'rels' —
    posixpath.splitext disagrees, which is why this exists."""
    base = posixpath.basename(part)
    return base.rsplit(".", 1)[1].lower() if "." in base else ""


def resolve(base_dir, target):
    """Resolve a rel Target against the owning part's directory. '' if unusable."""
    tgt = unquote(target.split("#", 1)[0].replace("\\", "/")).strip()
    if not tgt:
        return ""
    if tgt.startswith("/"):
        return posixpath.normpath(tgt[1:])
    return posixpath.normpath(posixpath.join(base_dir, tgt) if base_dir else tgt)


# ---- checks -----------------------------------------------------------------

def check_xml(pkg, rep):
    names = [n for n in pkg.names if n.endswith(".xml") or n.endswith(".rels")]
    for name in names:
        root, err = pkg.xml(name)
        if root is None:
            rep.fail("xml", name, "malformed",
                     f"Part {name} is not well-formed XML ({err}). PowerPoint will refuse the "
                     f"file or silently drop the part — regenerate it, and if it was hand-edited "
                     f"re-check the edit.")
    rep.note("xml", f"{len(names)} xml/rels parts parsed")


def check_content_types(pkg, rep):
    if CT_PART not in pkg.parts:
        rep.fail("content-types", CT_PART, "missing",
                 "[Content_Types].xml is missing. Without it the package is not an OOXML file "
                 "at all — re-export the deck.")
        return
    root, err = pkg.xml(CT_PART)
    if root is None:
        rep.fail("content-types", CT_PART, "malformed",
                 f"[Content_Types].xml does not parse ({err}). Fix it before trusting any other "
                 f"result here.")
        return
    defaults, overrides = {}, {}
    for el in root.findall(f"{{{NS_CT}}}Default"):
        ext, ctype = (el.get("Extension") or "").lower().lstrip("."), el.get("ContentType")
        if not ext or not ctype:
            rep.fail("content-types", CT_PART, "bad-default",
                     f"A <Default> entry in [Content_Types].xml is incomplete "
                     f"(Extension={el.get('Extension')!r}, ContentType={ctype!r}). Give it both "
                     f"attributes or delete it.")
            continue
        defaults[ext] = ctype
    for el in root.findall(f"{{{NS_CT}}}Override"):
        name, ctype = (el.get("PartName") or "").lstrip("/"), el.get("ContentType")
        if not name or not ctype:
            rep.fail("content-types", CT_PART, "bad-override",
                     f"An <Override> entry in [Content_Types].xml is incomplete "
                     f"(PartName={el.get('PartName')!r}, ContentType={ctype!r}). Give it both "
                     f"attributes or delete it.")
            continue
        overrides[name] = ctype
        if name not in pkg.parts:
            rep.warn("content-types", CT_PART, f"stale-override:{name}",
                     f'[Content_Types].xml has an <Override PartName="/{name}"> for a part that '
                     f"is not in the package. Harmless but stale — remove the override or add "
                     f"the part.")
    for part in pkg.names:
        if part == CT_PART:
            continue
        if part in overrides or ext_of(part) in defaults:
            continue
        rep.fail("content-types", part, "uncovered",
                 f"Part {part} has no content type. Add "
                 f'<Default Extension="{ext_of(part) or "???"}" ContentType="..."/> or '
                 f'<Override PartName="/{part}" ContentType="..."/> to [Content_Types].xml, or '
                 f"remove the part.")
    rep.note("content-types", f"{len(defaults)} defaults, {len(overrides)} overrides")


def check_relationships(pkg, rep):
    """-> (rel_index, targeted). rel_index: rels part -> {rId: (resolved, target, external)}."""
    rel_index, targeted, count = {}, set(), 0
    for name in sorted(n for n in pkg.names if n.endswith(".rels")):
        root, _ = pkg.xml(name)
        if root is None:
            rel_index[name] = {}
            continue                                    # already failed under [xml]
        base, table = owner_dir(name), {}
        for el in root.findall(f"{{{NS_PR}}}Relationship"):
            rid, target = el.get("Id") or "?", el.get("Target")
            count += 1
            if not target:
                rep.fail("relationships", name, f"no-target:{rid}",
                         f"Relationship {rid} in {name} has no Target attribute. Add "
                         f'Target="..." or delete the relationship.')
                continue
            if (el.get("TargetMode") or "") == "External":
                table[rid] = (None, target, True)
                continue
            resolved = resolve(base, target)
            table[rid] = (resolved, target, False)
            if not resolved or resolved.startswith(".."):
                rep.fail("relationships", name, f"escapes:{rid}",
                         f'Relationship {rid} in {name} has Target "{target}", which resolves '
                         f"outside the package root. Rewrite the Target relative to "
                         f'{base or "the package root"}/, or mark it TargetMode="External".')
            elif resolved not in pkg.parts:
                rep.fail("relationships", name, f"dangling:{rid}:{resolved}",
                         f"Relationship {rid} in {name} points at {target} which is not in the "
                         f"package. Add the {posixpath.basename(resolved)} part or remove the "
                         f'relationship (and any r:id="{rid}" reference to it in '
                         f'{owner_part(name) or "the owning part"}).')
            else:
                targeted.add(resolved)
        rel_index[name] = table
    rep.note("relationships", f"{count} relationships in {len(rel_index)} rels parts")
    return rel_index, targeted


def check_dangling_ids(pkg, rep, rel_index, slides):
    """Every r:id-ish attribute in a part must be defined in that part's own rels."""
    for part in sorted(n for n in pkg.names if n.endswith(".xml")):
        root, _ = pkg.xml(part)
        if root is None:
            continue
        used = {v for el in root.iter() for k, v in el.attrib.items()
                if k.startswith(f"{{{NS_R}}}") and RID_RE.match(v or "")}
        if not used:
            continue
        rels = rels_for(part)
        missing_note = "" if rels in pkg.parts else " (the rels part is missing entirely)"
        check = "slides" if part in slides else "relationships"
        for rid in sorted(used - set(rel_index.get(rels, {})), key=lambda s: (len(s), s)):
            rep.fail(check, part, f"undefined-rid:{rid}",
                     f"{part} references {rid} but {rels} does not define it{missing_note}. Add "
                     f'<Relationship Id="{rid}" Type="..." Target="..."/> to {rels}, or remove '
                     f"the reference from {posixpath.basename(part)}.")


def check_presentation(pkg, rep, rel_index):
    """-> ordered list of slide parts named by <p:sldIdLst>."""
    if PRES_PART not in pkg.parts:
        rep.fail("presentation", PRES_PART, "missing",
                 "ppt/presentation.xml is missing. It is the root of the deck — re-export; "
                 "there is nothing to repair.")
        return []
    root, err = pkg.xml(PRES_PART)
    if root is None:
        rep.fail("presentation", PRES_PART, "malformed",
                 f"ppt/presentation.xml does not parse ({err}), so slide order cannot be "
                 f"verified. Regenerate it (check any post-processing step that rewrites it, "
                 f"e.g. font embedding).")
        return []
    lst = root.find(f"{{{NS_P}}}sldIdLst")
    entries = list(lst) if lst is not None else []
    if not entries:
        rep.fail("presentation", PRES_PART, "empty-sldIdLst",
                 "ppt/presentation.xml has no <p:sldId> entries, so the deck opens with zero "
                 "slides. Add the <p:sldIdLst> entries for the slide parts, or stop shipping an "
                 "empty deck.")
        return []
    table = rel_index.get(PRES_RELS)
    if table is None:
        rep.fail("presentation", PRES_RELS, "missing-rels",
                 f"{PRES_RELS} is missing, so none of the {len(entries)} <p:sldId> entries can "
                 f"resolve. Add the relationship part.")
        return []
    slides = []
    for el in entries:
        sid, rid = el.get("id") or "?", el.get(f"{{{NS_R}}}id")
        if not rid:
            rep.fail("presentation", PRES_PART, f"no-rid:{sid}",
                     f'<p:sldId id="{sid}"> in ppt/presentation.xml has no r:id. Add r:id '
                     f"pointing at the slide's relationship, or remove the entry.")
            continue
        if rid not in table:
            rep.fail("presentation", PRES_PART, f"unknown-rid:{rid}",
                     f'<p:sldId id="{sid}" r:id="{rid}"> in ppt/presentation.xml has no matching '
                     f'relationship in {PRES_RELS}. Add <Relationship Id="{rid}" '
                     f'Type=".../slide" Target="slides/slideN.xml"/>, or remove the <p:sldId>.')
            continue
        resolved, target, external = table[rid]
        if external:
            rep.fail("presentation", PRES_PART, f"external-slide:{rid}",
                     f'<p:sldId id="{sid}" r:id="{rid}"> resolves to an External target '
                     f"({target}). A slide must be a part inside the package — fix the "
                     f"relationship in {PRES_RELS}.")
        elif resolved in pkg.parts:
            slides.append(resolved)
        # a resolved-but-absent target is already reported by [relationships]
    rep.note("presentation", f"{len(slides)}/{len(entries)} slide entries resolved")
    return slides


def check_slides(pkg, rep, rel_index, slides):
    layout_t = f"{NS_R}/slideLayout"
    for part in slides:
        rels = rels_for(part)
        if rels not in pkg.parts:
            rep.fail("slides", part, "missing-rels",
                     f"Slide {part} has no relationship part. Every slide needs at least a "
                     f"slideLayout relationship — add {rels} with "
                     f'<Relationship Id="rId1" Type="{layout_t}" '
                     f'Target="../slideLayouts/slideLayout1.xml"/>.')
            continue
        root, _ = pkg.xml(rels)
        types = ([el.get("Type") or "" for el in root.findall(f"{{{NS_PR}}}Relationship")]
                 if root is not None else [])
        if not any(t.endswith("/slideLayout") for t in types):
            rep.fail("slides", part, "no-layout-rel",
                     f"Slide {part} has no slideLayout relationship in {rels}. PowerPoint needs "
                     f'one to render placeholders and theme colours — add a Type="{layout_t}" '
                     f"relationship to an existing ppt/slideLayouts/slideLayoutN.xml.")
    for part in sorted(n for n in pkg.names if SLIDE_RE.match(n) and n not in set(slides)):
        rep.warn("slides", part, "orphan",
                 f"Slide part {part} is in the package but not reachable from <p:sldIdLst> in "
                 f"ppt/presentation.xml, so it will never be shown. Add a <p:sldId> entry for "
                 f"it or delete the part.")
    check_dangling_ids(pkg, rep, rel_index, set(slides))
    rep.note("slides", f"{len(slides)} slides checked")


def check_media(pkg, rep, targeted):
    media = [n for n in pkg.names if n.startswith(MEDIA_DIRS)]
    dangling = sorted(n for n in media if n not in targeted)
    for part in dangling:
        rep.warn("media", part, "unreferenced",
                 f"{part} is in the package but no relationship points at it. It is dead weight "
                 f"in the file — delete the part (and its [Content_Types] entry if it was an "
                 f"Override) unless something references it dynamically.")
    rep.note("media", f"{len(media)} media/embedded parts, {len(dangling)} unreferenced")


def check_charts(pkg, rep):
    charts = sorted(n for n in pkg.names if CHART_RE.match(n))
    for part in charts:
        root, _ = pkg.xml(part)
        if root is None:
            continue                                    # already failed under [xml]
        if next(root.iter(f"{{{NS_C}}}chart"), None) is None:
            rep.fail("charts", part, "no-c-chart",
                     f"Chart part {part} parses but contains no <c:chart> element, so PowerPoint "
                     f"will show an empty chart frame. Regenerate the chart XML (a c:chartSpace "
                     f"must hold a c:chart) or remove the graphicFrame that points at it.")
    rep.note("charts", f"{len(charts)} chart parts")


def analyze(path):
    """Run every check against one package. Never raises for a bad file."""
    rep = Report()
    try:
        pkg = Package(path)
    except (zipfile.BadZipFile, OSError) as exc:
        rep.fail("package", path, "unreadable",
                 f"{path} could not be opened as a zip container ({exc}). A .pptx is a zip — "
                 f"check you are pointing at the right file and re-export it.")
        return rep
    bad = None
    try:
        bad = pkg.zf.testzip()
    except Exception as exc:
        rep.fail("package", path, "crc-scan",
                 f"{path} could not be fully read ({exc}). The archive is damaged — re-export "
                 f"the deck.")
    if bad:
        rep.fail("package", bad, "crc",
                 f"Part {bad} fails its CRC check, so the stored bytes are corrupt. Re-export "
                 f"the deck; nothing downstream can trust this part.")
    rep.note("package", f"{len(pkg.names)} parts")
    check_xml(pkg, rep)
    check_content_types(pkg, rep)
    rel_index, targeted = check_relationships(pkg, rep)
    slides = check_presentation(pkg, rep, rel_index)
    check_slides(pkg, rep, rel_index, slides)
    check_media(pkg, rep, targeted)
    check_charts(pkg, rep)
    return rep


# ---- output -----------------------------------------------------------------

def emit(path, rep, suppressed, original):
    print(f"validate_pptx: {path}")
    if original:
        print(f"  baseline: {original} (failures it also has are suppressed)")
    print()
    for check in CHECK_ORDER:
        items = [i for i in rep.items if i.check == check]
        fails = [i for i in items if i.sev == "FAIL"]
        warns = [i for i in items if i.sev == "WARN"]
        status = "ok" if not fails else f"{len(fails)} failure(s)"
        if warns:
            status += f", {len(warns)} warning(s)"
        note = rep.notes.get(check, "")
        print(f"[{check}] {status}" + (f" — {note}" if note else ""))
        for item in fails + warns:
            print(f"  {item.sev}  {item.msg}")
    if suppressed:
        print(f"\nSuppressed — also present in {original}: {len(suppressed)}")
        for item in suppressed:
            print(f"  [{item.check}] {item.msg}")
    nf = len(rep.failures())
    nw = len([i for i in rep.items if i.sev == "WARN"])
    print(f"\nSummary: {len(CHECK_ORDER)} checks, {nf} failure(s), {nw} warning(s), "
          f"{len(suppressed)} suppressed — {'FAIL' if nf else 'PASS'}")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Validate the OOXML package structure of a .pptx (read-only).")
    ap.add_argument("deck", help="the .pptx to validate")
    ap.add_argument("--original", metavar="TEMPLATE",
                    help="template the deck was built from; failures it also has are "
                         "reported separately instead of failing the run")
    args = ap.parse_args(argv)

    rep = analyze(args.deck)
    suppressed = []
    if args.original:
        known = {signature(i) for i in analyze(args.original).failures()}
        keep = []
        for item in rep.items:
            target = suppressed if item.sev == "FAIL" and signature(item) in known else keep
            target.append(item)
        rep.items = keep
    emit(args.deck, rep, suppressed, args.original)
    return 1 if rep.failures() else 0


if __name__ == "__main__":
    sys.exit(main())
