#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path

from patterns import (
    PATTERN_MAP,
    generate_all,
    gen_a00,
    gen_a01,
    gen_a02,
    gen_a03,
    gen_a04,
    gen_a05,
    gen_a06,
    gen_a07,
)


class PatternTests(unittest.TestCase):
    def test_solids(self):
        self.assertEqual(set(gen_a00(8, 4)), {0})
        self.assertEqual(set(gen_a01(8, 4)), {255})
        self.assertEqual(set(gen_a02(8, 4)), {128})

    def test_gray_steps_cover_black_and_white(self):
        row = gen_a03(110, 1)
        values = sorted(set(row))
        self.assertEqual(len(values), 11)
        self.assertEqual(values[0], 0)
        self.assertEqual(values[-1], 255)

    def test_horizontal_ramp_endpoints(self):
        row = gen_a04(256, 1)
        self.assertEqual(row[0], 0)
        self.assertEqual(row[-1], 255)
        self.assertTrue(all(a <= b for a, b in zip(row, row[1:])))

    def test_vertical_ramp_endpoints(self):
        pixels = gen_a05(4, 256)
        self.assertEqual(pixels[0], 0)
        self.assertEqual(pixels[-1], 255)
        self.assertEqual(pixels[-4:], bytes([255]) * 4)

    def test_near_black_levels(self):
        values = sorted(set(gen_a06(60, 1)))
        self.assertEqual(values, [0, 5, 10, 15, 20, 26])

    def test_near_white_levels(self):
        values = sorted(set(gen_a07(60, 1)))
        self.assertEqual(values, [230, 235, 240, 245, 250, 255])

    def test_manifest_and_hashes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifest = generate_all(root, 64, 48)
            self.assertEqual(len(manifest["patterns"]), 8)
            disk = json.loads((root / "manifest.json").read_text())
            self.assertEqual(disk["width"], 64)
            self.assertEqual(disk["height"], 48)
            for item in disk["patterns"]:
                self.assertEqual(len(item["sha256"]), 64)
                self.assertTrue((root / item["file"]).exists())

    def test_catalog_ids(self):
        self.assertEqual(list(PATTERN_MAP), [f"A{i:02d}" for i in range(8)])


if __name__ == "__main__":
    unittest.main()
