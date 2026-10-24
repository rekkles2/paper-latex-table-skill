import unittest,tempfile,json,hashlib
from pathlib import Path
from export_public import public_markdown
from validate_gallery import validate
class PublicGalleryTests(unittest.TestCase):
 def test_local_content_and_derivatives_removed(self):
  text='public\n<!-- LOCAL-ONLY:BEGIN -->\n![x](assets/cases/local/x/reproduced.png)\n<!-- LOCAL-ONLY:END -->\nend\n'
  self.assertEqual(public_markdown(text),'public\nend\n')
 def test_malformed_boundaries_fail_closed(self):
  for text in ['<!-- LOCAL-ONLY:BEGIN -->\nx','<!-- LOCAL-ONLY:END -->\n','<!-- LOCAL-ONLY:BEGIN -->\n<!-- LOCAL-ONLY:BEGIN -->\n']:
   with self.subTest(text=text),self.assertRaises(ValueError):public_markdown(text)
 def test_private_links_cannot_escape_markers(self):
  for text in ['![x](assets/cases/local/x.png)','<img src="assets/cases/local/x.png">','[source](../assets/cases/local/x/table.tex)']:
   with self.subTest(text=text),self.assertRaises(ValueError):public_markdown(text)
 def test_public_image_survives(self):
  t='![example](docs/images/public/wide.png)\n';self.assertEqual(public_markdown(t),t)
class PairIntegrityTests(unittest.TestCase):
 def test_missing_and_stale_pairs_cannot_pass(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'a.tex').write_text('source');(root/'a.png').write_bytes(b'preview')
   record={'id':'demo','tex':'a.tex','figure':'a.png','sha256':{'tex':hashlib.sha256(b'source').hexdigest(),'figure':hashlib.sha256(b'preview').hexdigest()}}
   index=root/'index.json';index.write_text(json.dumps({'examples':[record]}));self.assertEqual(len(validate(index,root)),1)
   (root/'a.png').write_bytes(b'stale')
   with self.assertRaises(ValueError):validate(index,root)
   (root/'a.png').unlink()
   with self.assertRaises(ValueError):validate(index,root)
 def test_path_traversal_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);index=root/'index.json';index.write_text(json.dumps({'examples':[{'id':'x','tex':'../outside.tex','figure':'x.png','sha256':{}}]}))
   with self.assertRaises(ValueError):validate(index,root)
if __name__=='__main__':unittest.main()
