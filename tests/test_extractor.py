import os
import unittest
import pdftotext

from damnboleto import BASE_DIR, Extractor


class ExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.assets_dir = os.path.join(BASE_DIR, 'tests/assets')

    def test_load_file(self):
        filepath = '{}/{}'.format(self.assets_dir, 'santander.pdf')
        pdf = Extractor._load_file(filepath=filepath, password='')
        self.assertIsInstance(pdf, pdftotext.PDF)

    def test_sanitize_barcode(self):
        dirty_barcode = '03399.63290 64000.000006 00125.201020 4 56140000017832'
        expected = '03399 63290 64000 000006 00125 201020 4 56140000017832'
        result = Extractor._sanitize_barcode(dirty_barcode)
        self.assertEqual(expected, result)

    def test_extract_barcode(self):
        filepath = '{}/{}'.format(self.assets_dir, 'santander.pdf')
        extractor = Extractor(filepath=filepath)

        expected = '03399 63290 64000 000006 00125 201020 4 56140000017832'
        self.assertEqual(expected, extractor.extract_barcode())

    def test_extract_bank_code(self):
        filepath = '{}/{}'.format(self.assets_dir, 'santander.pdf')
        extractor = Extractor(filepath=filepath)

        barcode = '03399 63290 64000 000006 00125 201020 4 56140000017832'
        expected = '033'

        self.assertEqual(expected, extractor.extract_bank_code(barcode))

    def test_extract_bank(self):
        filepath = '{}/{}'.format(self.assets_dir, 'santander.pdf')
        extractor = Extractor(filepath=filepath)
        bank_code = '033'

        expected = 'Banco Santander (Brasil) S.A.'

        self.assertEqual(expected, extractor.extract_bank(bank_code))

    def test_extract_all(self):
        filepath = '{}/{}'.format(self.assets_dir, 'santander.pdf')
        extractor = Extractor(filepath=filepath)

        expected = {
            'barcode': '03399 63290 64000 000006 00125 201020 4 56140000017832',
            'bank_code': '033',
            'bank': 'Banco Santander (Brasil) S.A.'
        }

        self.assertDictEqual(expected, extractor.extract_all())
