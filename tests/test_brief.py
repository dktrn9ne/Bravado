import copy
import json
import unittest
from pathlib import Path
from brief import validate_brief, TEXT_FIELDS

ROOT = Path(__file__).resolve().parents[1]

class BriefTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT/'projects/cadence.json').read_text())

    def test_valid_sample_is_unchanged(self):
        self.assertIs(validate_brief(self.data), self.data)

    def test_every_used_text_field_is_required(self):
        for group, fields in TEXT_FIELDS.items():
            for field in fields.split():
                data = copy.deepcopy(self.data)
                node = data
                for part in group.split('.'):node = node[part]
                del node[field]
                with self.subTest(field=f'{group}.{field}'), self.assertRaisesRegex(ValueError, f'{group}.{field}'):
                    validate_brief(data)

    def test_reject_invalid_numbers(self):
        for key in ('period_days', 'interval_seconds', 'weekly_total', 'starting_amount'):
            invalid = [True, None, '15', float('nan'), float('inf'), -1]
            if key in ('period_days','interval_seconds'):invalid += [1.5, 0]
            for item in invalid:
                data = copy.deepcopy(self.data);data['example'][key] = item
                with self.subTest(key=key, value=item), self.assertRaisesRegex(ValueError,key):
                    validate_brief(data)

    def test_malformed_cards_and_labels(self):
        for group, key, items in [('flow','audiences',[None, ['one','two','three'], [['a','b']]*2, [['a',3]]*3]),('proof','verbs',[None, 'abc', ['one'], ['a','b',3]])]:
            for item in items:
                data = copy.deepcopy(self.data);data['story'][group][key] = item
                with self.subTest(key=key, value=item), self.assertRaises(ValueError):validate_brief(data)

    def test_palette(self):
        for item in (None, '#zzz123', 'ffffff', '#fff', 123):
            self.data['palette']['forest'] = item
            with self.subTest(value=item), self.assertRaisesRegex(ValueError, 'palette.forest'):
                validate_brief(self.data)

    def test_empty_optional_monogram_rejected(self):
        self.data['brand']['monogram'] = ''
        with self.assertRaisesRegex(ValueError,'monogram'):validate_brief(self.data)
