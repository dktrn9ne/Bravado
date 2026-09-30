import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from PIL import ImageFont
import render

ROOT = Path(__file__).resolve().parents[1]

class RenderTests(unittest.TestCase):
    def test_custom_palette_is_used_by_default_arguments(self):
        with patch.multiple(render, CREAM='#f2f3f4',FOREST='#123456',MUTED='#789abc',CLAY='#ff3344'), patch.object(render,'font',return_value=ImageFont.load_default()):
            c = render.Canvas()
            self.assertEqual(c.im.getpixel((0,0)),(242,243,244))
            c.line([(10,10),(20,10)])
            self.assertEqual(c.im.getpixel((22,15)),(18,52,86))
            with patch.object(c.d,'text') as text:
                c.text(1,1,'example');self.assertEqual(text.call_args.kwargs['fill'],'#123456')
                c.label(1,1,'label');self.assertEqual(text.call_args.kwargs['fill'],'#789abc')
            c.pill(100,100,'label')
            self.assertEqual(c.im.getpixel((160,155)),(18,52,86))

    def test_loading_second_brief_updates_background(self):
        with tempfile.TemporaryDirectory() as temp:
            data=json.loads((ROOT/'projects/cadence.json').read_text())
            path=Path(temp)/'brief.json'
            for color in ('#112233','#ddeeff'):
                data['palette']['cream']=color;path.write_text(json.dumps(data))
                render.load(path,temp)
                self.assertEqual(render.Canvas().im.getpixel((0,0)),render.rgb(color))
        render.load(ROOT/'projects/cadence.json',tempfile.gettempdir())

    def test_starter_files_match_sources(self):
        for name in ('render.py','brief.py','verify_export.py','inspect_source.py','setup_fonts.py','requirements.txt','projects/cadence.json'):
            with self.subTest(name=name):
                self.assertEqual((ROOT/name).read_bytes(),(ROOT/'skill/assets/starter'/name).read_bytes())
