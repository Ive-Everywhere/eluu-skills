#!/usr/bin/env python3
# Copyright 2026 Eluu Labs — Apache-2.0 (see ../LICENSE)
"""
Tests for validate_pptx. Standard library unittest, no pytest, no fixtures on disk:
every package is built here as a dict of {part name -> bytes} and zipped into a
temp dir, so the suite runs anywhere and the broken cases are legible.

    python3 test_validate_pptx.py            # or: python3 -m unittest -v

Note on --original suppression: signatures collapse digit runs, so slide3.xml in a
deck matches slide1.xml in the template (python-pptx renumbers generated parts).
That is intentionally loose and can over-suppress — a deck whose image9.png rel is
broken is suppressed by a template whose image1.png rel is broken, in the same
check on the same kind of part. Tighten `signature()` if that ever bites.
"""
import os, shutil, tempfile, unittest, zipfile
import io, contextlib

import validate_pptx as V

R  = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"


def rels(*entries):
    body = "".join(
        f'<Relationship Id="{i}" Type="{t}" Target="{g}"'
        + (f' TargetMode="{m}"' if m else "") + "/>"
        for i, t, g, m in entries)
    return f'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="{PR}">{body}</Relationships>'.encode()


def content_types(defaults, overrides):
    d = "".join(f'<Default Extension="{e}" ContentType="{c}"/>' for e, c in defaults)
    o = "".join(f'<Override PartName="/{p}" ContentType="{c}"/>' for p, c in overrides)
    return f'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="{CT}">{d}{o}</Types>'.encode()


P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
C = "http://schemas.openxmlformats.org/drawingml/2006/chart"
ML = "application/vnd.openxmlformats-officedocument.presentationml"


def clean_package():
    """A minimal package that every check should be happy with."""
    pkg = {}
    pkg["[Content_Types].xml"] = content_types(
        [("rels", "application/vnd.openxmlformats-package.relationships+xml"),
         ("xml", "application/xml"), ("png", "image/png")],
        [("ppt/presentation.xml", f"{ML}.presentation.main+xml"),
         ("ppt/slides/slide1.xml", f"{ML}.slide+xml"),
         ("ppt/slideLayouts/slideLayout1.xml", f"{ML}.slideLayout+xml"),
         ("ppt/slideMasters/slideMaster1.xml", f"{ML}.slideMaster+xml"),
         ("ppt/theme/theme1.xml", "application/vnd.openxmlformats-officedocument.theme+xml")])
    pkg["_rels/.rels"] = rels(("rId1", f"{R}/officeDocument", "ppt/presentation.xml", None))
    pkg["ppt/presentation.xml"] = (
        f'<?xml version="1.0"?><p:presentation xmlns:p="{P}" xmlns:r="{R}">'
        f'<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        f'<p:sldIdLst><p:sldId id="256" r:id="rId2"/></p:sldIdLst>'
        f'</p:presentation>').encode()
    pkg["ppt/_rels/presentation.xml.rels"] = rels(
        ("rId1", f"{R}/slideMaster", "slideMasters/slideMaster1.xml", None),
        ("rId2", f"{R}/slide", "slides/slide1.xml", None),
        ("rId3", f"{R}/theme", "theme/theme1.xml", None))
    # the slide uses a relative ../media/ target, the case that breaks most often
    pkg["ppt/slides/slide1.xml"] = (
        f'<?xml version="1.0"?><p:sld xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}">'
        f'<p:cSld><p:spTree><p:pic><p:blipFill><a:blip r:embed="rId2"/></p:blipFill>'
        f'</p:pic></p:spTree></p:cSld></p:sld>').encode()
    pkg["ppt/slides/_rels/slide1.xml.rels"] = rels(
        ("rId1", f"{R}/slideLayout", "../slideLayouts/slideLayout1.xml", None),
        ("rId2", f"{R}/image", "../media/image1.png", None),
        ("rId3", f"{R}/hyperlink", "https://eluu.example", "External"))
    pkg["ppt/slideLayouts/slideLayout1.xml"] = f'<?xml version="1.0"?><p:sldLayout xmlns:p="{P}"/>'.encode()
    pkg["ppt/slideLayouts/_rels/slideLayout1.xml.rels"] = rels(
        ("rId1", f"{R}/slideMaster", "../slideMasters/slideMaster1.xml", None))
    pkg["ppt/slideMasters/slideMaster1.xml"] = f'<?xml version="1.0"?><p:sldMaster xmlns:p="{P}"/>'.encode()
    pkg["ppt/slideMasters/_rels/slideMaster1.xml.rels"] = rels(
        ("rId1", f"{R}/slideLayout", "../slideLayouts/slideLayout1.xml", None),
        ("rId2", f"{R}/theme", "../theme/theme1.xml", None))
    pkg["ppt/theme/theme1.xml"] = f'<?xml version="1.0"?><a:theme xmlns:a="{A}"/>'.encode()
    pkg["ppt/media/image1.png"] = b"\x89PNG\r\n\x1a\n-not-a-real-png-"
    return pkg


class Base(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="validate_pptx_")
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)

    def write(self, parts, name="deck.pptx"):
        path = os.path.join(self.dir, name)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
            for part, data in parts.items():
                zf.writestr(part, data)
        return path

    def run_cli(self, *argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = V.main(list(argv))
        return code, buf.getvalue()

    def fails(self, report, check=None):
        return [i for i in report.failures() if check is None or i.check == check]

    def warns(self, report, check=None):
        return [i for i in report.items
                if i.sev == "WARN" and (check is None or i.check == check)]


class TestCleanPackage(Base):
    def test_clean_package_passes(self):
        path = self.write(clean_package())
        rep = V.analyze(path)
        self.assertEqual([], self.fails(rep), "\n".join(i.msg for i in self.fails(rep)))
        self.assertEqual([], self.warns(rep), "\n".join(i.msg for i in self.warns(rep)))

    def test_clean_package_exits_zero(self):
        code, out = self.run_cli(self.write(clean_package()))
        self.assertEqual(0, code, out)
        self.assertIn("PASS", out)
        for check in V.CHECK_ORDER:
            self.assertIn(f"[{check}] ok", out)

    def test_external_target_is_not_resolved(self):
        rep = V.analyze(self.write(clean_package()))
        self.assertFalse([i for i in rep.items if "eluu.example" in i.msg])


class TestRelationships(Base):
    def test_dangling_relationship_fails(self):
        parts = clean_package()
        parts["ppt/slides/_rels/slide1.xml.rels"] = rels(
            ("rId1", f"{R}/slideLayout", "../slideLayouts/slideLayout1.xml", None),
            ("rId2", f"{R}/image", "../media/image9.png", None))
        code, out = self.run_cli(self.write(parts))
        self.assertEqual(1, code, out)
        rep = V.analyze(self.write(parts))
        msgs = [i.msg for i in self.fails(rep, "relationships")]
        self.assertEqual(1, len(msgs), msgs)
        self.assertIn("../media/image9.png which is not in the package", msgs[0])
        self.assertIn("Add the image9.png part or remove the relationship", msgs[0])

    def test_relative_parent_targets_resolve(self):
        """../slideLayouts/... from ppt/slides/ must land on ppt/slideLayouts/..."""
        self.assertEqual("ppt/slideLayouts/slideLayout1.xml",
                         V.resolve("ppt/slides", "../slideLayouts/slideLayout1.xml"))
        self.assertEqual("ppt/presentation.xml", V.resolve("", "ppt/presentation.xml"))
        self.assertEqual("ppt/media/i.png", V.resolve("ppt/slides", "/ppt/media/i.png"))
        self.assertEqual("ppt/media/my image.png",
                         V.resolve("ppt/slides", "../media/my%20image.png"))
        self.assertEqual("ppt/slides", V.owner_dir("ppt/slides/_rels/slide1.xml.rels"))
        self.assertEqual("", V.owner_dir("_rels/.rels"))
        self.assertEqual("ppt/slides/slide1.xml", V.owner_part("ppt/slides/_rels/slide1.xml.rels"))

    def test_target_escaping_package_root_fails(self):
        parts = clean_package()
        parts["ppt/slides/_rels/slide1.xml.rels"] = rels(
            ("rId1", f"{R}/slideLayout", "../slideLayouts/slideLayout1.xml", None),
            ("rId2", f"{R}/image", "../../../media/image1.png", None))
        rep = V.analyze(self.write(parts))
        msgs = [i.msg for i in self.fails(rep, "relationships")]
        self.assertTrue(any("outside the package root" in m for m in msgs), msgs)

    def test_undefined_rid_in_slide_fails(self):
        parts = clean_package()
        parts["ppt/slides/_rels/slide1.xml.rels"] = rels(
            ("rId1", f"{R}/slideLayout", "../slideLayouts/slideLayout1.xml", None))
        rep = V.analyze(self.write(parts))
        msgs = [i.msg for i in self.fails(rep, "slides")]
        self.assertTrue(any("references rId2" in m for m in msgs), msgs)


class TestContentTypes(Base):
    def test_missing_override_fails(self):
        parts = clean_package()
        parts["[Content_Types].xml"] = content_types(
            [("rels", "application/vnd.openxmlformats-package.relationships+xml"),
             ("png", "image/png")],                     # no xml Default either
            [("ppt/presentation.xml", f"{ML}.presentation.main+xml")])
        code, out = self.run_cli(self.write(parts))
        self.assertEqual(1, code, out)
        rep = V.analyze(self.write(parts))
        msgs = [i.msg for i in self.fails(rep, "content-types")]
        self.assertTrue(any("ppt/slides/slide1.xml has no content type" in m for m in msgs), msgs)
        self.assertTrue(any('<Override PartName="/ppt/slides/slide1.xml"' in m for m in msgs), msgs)

    def test_missing_content_types_part_fails(self):
        parts = clean_package()
        del parts["[Content_Types].xml"]
        rep = V.analyze(self.write(parts))
        self.assertTrue(any("[Content_Types].xml is missing" in i.msg
                            for i in self.fails(rep, "content-types")))

    def test_stale_override_only_warns(self):
        parts = clean_package()
        parts["[Content_Types].xml"] = parts["[Content_Types].xml"].replace(
            b"</Types>", f'<Override PartName="/ppt/slides/slide7.xml" ContentType="{ML}.slide+xml"/></Types>'.encode())
        code, out = self.run_cli(self.write(parts))
        self.assertEqual(0, code, out)
        self.assertIn("stale", "".join(i.detail for i in self.warns(V.analyze(self.write(parts)))))


class TestXmlWellFormedness(Base):
    def test_malformed_xml_fails(self):
        parts = clean_package()
        parts["ppt/slides/slide1.xml"] = b'<?xml version="1.0"?><p:sld><p:cSld>'
        code, out = self.run_cli(self.write(parts))
        self.assertEqual(1, code, out)
        rep = V.analyze(self.write(parts))
        msgs = [i.msg for i in self.fails(rep, "xml")]
        self.assertTrue(any("ppt/slides/slide1.xml is not well-formed XML" in m for m in msgs), msgs)

    def test_malformed_rels_fails(self):
        parts = clean_package()
        parts["ppt/slides/_rels/slide1.xml.rels"] = b"<Relationships><oops>"
        rep = V.analyze(self.write(parts))
        self.assertTrue(any(".rels is not well-formed XML" in i.msg for i in self.fails(rep, "xml")))

    def test_not_a_zip_fails(self):
        path = os.path.join(self.dir, "bogus.pptx")
        with open(path, "wb") as fh:
            fh.write(b"this is not a zip")
        code, out = self.run_cli(path)
        self.assertEqual(1, code, out)
        self.assertIn("could not be opened as a zip container", out)


class TestPresentationAndSlides(Base):
    def test_sldid_without_relationship_fails(self):
        parts = clean_package()
        parts["ppt/presentation.xml"] = parts["ppt/presentation.xml"].replace(
            b'r:id="rId2"/></p:sldIdLst>', b'r:id="rId2"/><p:sldId id="257" r:id="rId9"/></p:sldIdLst>')
        rep = V.analyze(self.write(parts))
        msgs = [i.msg for i in self.fails(rep, "presentation")]
        self.assertEqual(1, len(msgs), msgs)
        self.assertIn('r:id="rId9"', msgs[0])
        self.assertIn("has no matching relationship", msgs[0])

    def test_empty_sldidlst_fails(self):
        parts = clean_package()
        parts["ppt/presentation.xml"] = (
            f'<?xml version="1.0"?><p:presentation xmlns:p="{P}" xmlns:r="{R}">'
            f'<p:sldIdLst/></p:presentation>').encode()
        rep = V.analyze(self.write(parts))
        self.assertTrue(any("opens with zero slides" in i.msg
                            for i in self.fails(rep, "presentation")))

    def test_slide_without_rels_part_fails(self):
        parts = clean_package()
        del parts["ppt/slides/_rels/slide1.xml.rels"]
        rep = V.analyze(self.write(parts))
        msgs = [i.msg for i in self.fails(rep, "slides")]
        self.assertTrue(any("has no relationship part" in m for m in msgs), msgs)

    def test_slide_without_layout_relationship_fails(self):
        parts = clean_package()
        parts["ppt/slides/_rels/slide1.xml.rels"] = rels(
            ("rId2", f"{R}/image", "../media/image1.png", None))
        rep = V.analyze(self.write(parts))
        self.assertTrue(any("no slideLayout relationship" in i.msg
                            for i in self.fails(rep, "slides")))

    def test_orphan_slide_part_warns_only(self):
        parts = clean_package()
        parts["ppt/slides/slide2.xml"] = parts["ppt/slides/slide1.xml"]
        parts["ppt/slides/_rels/slide2.xml.rels"] = parts["ppt/slides/_rels/slide1.xml.rels"]
        parts["[Content_Types].xml"] = parts["[Content_Types].xml"].replace(
            b"</Types>", f'<Override PartName="/ppt/slides/slide2.xml" ContentType="{ML}.slide+xml"/></Types>'.encode())
        code, out = self.run_cli(self.write(parts))
        self.assertEqual(0, code, out)
        self.assertTrue(any("not reachable from" in i.msg for i in self.warns(V.analyze(self.write(parts)))))


class TestMedia(Base):
    def test_dangling_media_warns_but_does_not_fail(self):
        parts = clean_package()
        parts["ppt/media/image7.png"] = b"\x89PNG\r\n\x1a\n-orphan-"
        code, out = self.run_cli(self.write(parts))
        self.assertEqual(0, code, out)
        rep = V.analyze(self.write(parts))
        self.assertEqual([], self.fails(rep), "\n".join(i.msg for i in self.fails(rep)))
        msgs = [i.msg for i in self.warns(rep, "media")]
        self.assertEqual(1, len(msgs), msgs)
        self.assertIn("ppt/media/image7.png is in the package but no relationship", msgs[0])
        self.assertIn("WARN", out)


class TestCharts(Base):
    def chart_package(self, chart_xml):
        parts = clean_package()
        parts["ppt/charts/chart1.xml"] = chart_xml
        parts["ppt/slides/_rels/slide1.xml.rels"] = rels(
            ("rId1", f"{R}/slideLayout", "../slideLayouts/slideLayout1.xml", None),
            ("rId2", f"{R}/image", "../media/image1.png", None),
            ("rId4", f"{R}/chart", "../charts/chart1.xml", None))
        return parts

    def test_chart_with_c_chart_passes(self):
        parts = self.chart_package(
            f'<?xml version="1.0"?><c:chartSpace xmlns:c="{C}"><c:chart><c:plotArea/>'
            f'</c:chart></c:chartSpace>'.encode())
        rep = V.analyze(self.write(parts))
        self.assertEqual([], self.fails(rep), "\n".join(i.msg for i in self.fails(rep)))

    def test_chart_without_c_chart_fails(self):
        parts = self.chart_package(
            f'<?xml version="1.0"?><c:chartSpace xmlns:c="{C}"><c:externalData/></c:chartSpace>'.encode())
        rep = V.analyze(self.write(parts))
        msgs = [i.msg for i in self.fails(rep, "charts")]
        self.assertEqual(1, len(msgs), msgs)
        self.assertIn("contains no <c:chart> element", msgs[0])


class TestOriginalSuppression(Base):
    def broken(self, name):
        """Package with a dangling image rel — the shape of an inherited defect."""
        parts = clean_package()
        parts["ppt/slides/_rels/slide1.xml.rels"] = rels(
            ("rId1", f"{R}/slideLayout", "../slideLayouts/slideLayout1.xml", None),
            ("rId2", f"{R}/image", "../media/image9.png", None))
        return self.write(parts, name)

    def test_shared_failure_is_suppressed(self):
        deck, template = self.broken("deck.pptx"), self.broken("template.pptx")
        code, out = self.run_cli(deck)
        self.assertEqual(1, code, out)
        code, out = self.run_cli(deck, "--original", template)
        self.assertEqual(0, code, out)
        self.assertIn("Suppressed", out)
        self.assertIn("1 suppressed", out)
        self.assertIn("[relationships] ok", out)

    def test_deck_only_failure_still_fails(self):
        template = self.write(clean_package(), "template.pptx")
        deck = self.broken("deck.pptx")
        code, out = self.run_cli(deck, "--original", template)
        self.assertEqual(1, code, out)
        self.assertIn("image9.png", out)
        self.assertIn("0 suppressed", out)

    def test_warnings_are_never_suppressed(self):
        parts = clean_package()
        parts["ppt/media/image7.png"] = b"orphan"
        deck = self.write(parts, "deck.pptx")
        template = self.write(parts, "template.pptx")
        code, out = self.run_cli(deck, "--original", template)
        self.assertEqual(0, code, out)
        self.assertIn("image7.png", out)
        self.assertIn("1 warning(s)", out)

    def test_unreadable_original_does_not_crash(self):
        deck = self.write(clean_package())
        missing = os.path.join(self.dir, "nope.pptx")
        code, out = self.run_cli(deck, "--original", missing)
        self.assertEqual(0, code, out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
