import json
from pathlib import Path
import tempfile
import unittest

from gallery_export import check_private_links, enhance_entries


class GalleryExportTests(unittest.TestCase):
    def test_scrubs_existing_docs_catalog_without_public_directory(self):
        catalog = {
            "examples": [
                {"name": "private", "private_reference": True},
                {
                    "name": "safe",
                    "dependencies": [
                        {"source": "assets/cases/local/private.tex"},
                        {"source": "examples/references/secret.tex"},
                        {"source": "examples/public/figure.png"},
                    ],
                },
            ]
        }
        key = "paper-latex-table-skill/docs/example-catalog.json"
        entries = {key: json.dumps(catalog).encode("utf-8")}

        with tempfile.TemporaryDirectory() as temporary_directory:
            result = enhance_entries(entries, Path(temporary_directory))

        cleaned_text = result[key].decode("utf-8")
        cleaned = json.loads(cleaned_text)
        self.assertEqual(
            cleaned,
            {
                "examples": [
                    {
                        "name": "safe",
                        "dependencies": [
                            {},
                            {},
                            {"source": "examples/public/figure.png"},
                        ],
                    }
                ]
            },
        )
        self.assertNotIn("private", cleaned_text)
        self.assertNotIn("examples/references", cleaned_text)
        self.assertNotIn("assets/cases/local", cleaned_text)

    def test_public_scan_omits_hidden_and_unknown_files(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            public = root / "examples" / "public"
            public.mkdir(parents=True)
            (public / "visible.tex").write_text(
                "\\begin{document}safe\\end{document}", encoding="utf-8"
            )
            (public / "notes.txt").write_text(
                "not an export asset", encoding="utf-8"
            )
            hidden = public / ".private"
            hidden.mkdir()
            (hidden / "secret.png").write_bytes(b"secret")
            cache = public / "__pycache__"
            cache.mkdir()
            (cache / "ignored.png").write_bytes(b"ignored")
            entries = {}

            enhance_entries(entries, root)

        self.assertIn(
            "paper-latex-table-skill/examples/public/visible.tex", entries
        )
        self.assertFalse(any("notes.txt" in name for name in entries))
        self.assertFalse(
            any(".private" in name or "__pycache__" in name for name in entries)
        )

    def test_public_markdown_check_rejects_private_links_and_returns_clean_text(self):
        cleaned = "# Gallery\n\n[Public example](examples/public/demo.tex)\n"

        self.assertIs(check_private_links(cleaned), cleaned)
        with self.assertRaisesRegex(ValueError, "private reference"):
            check_private_links("[Local](examples/references/secret.tex)")
        with self.assertRaisesRegex(ValueError, "private reference"):
            check_private_links(
                '<a href="assets/cases/local/private.tex">local</a>'
            )


if __name__ == "__main__":
    unittest.main()
