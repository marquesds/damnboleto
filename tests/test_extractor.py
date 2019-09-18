import os
import unittest
import pdftotext

from damnboleto import BASE_DIR, Extractor
from damnboleto.exceptions import BarcodeNotFound


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

    def test_extract_empty_barcode(self):
        filepath = '{}/{}'.format(self.assets_dir, 'dummy.pdf')
        with self.assertRaises(BarcodeNotFound):
            Extractor(filepath=filepath)

    def test_extract_bank_code(self):
        filepath = '{}/{}'.format(self.assets_dir, 'santander.pdf')
        extractor = Extractor(filepath=filepath)

        expected = '033'
        self.assertEqual(expected, extractor.extract_bank_code())

    def test_extract_bank(self):
        filepath = '{}/{}'.format(self.assets_dir, 'santander.pdf')
        extractor = Extractor(filepath=filepath)

        expected = 'Banco Santander (Brasil) S.A.'
        self.assertEqual(expected, extractor.extract_bank())

    def test_extract_boleto_amount(self):
        filepath = '{}/{}'.format(self.assets_dir, 'santander.pdf')
        extractor = Extractor(filepath=filepath)

        expected = 178.32
        self.assertEqual(expected, extractor.extract_amount())

    def test_extract_boleto_amount_with_zeros(self):
        filepath = '{}/{}'.format(self.assets_dir, 'santander.pdf')
        extractor = Extractor(filepath=filepath)
        extractor._barcode = '23790 46101 90000 001116 02012 189904 1 74000000080000'

        expected = 800.0
        self.assertEqual(expected, extractor.extract_amount())

    def test_extract_due_date(self):
        filepath = '{}/{}'.format(self.assets_dir, 'santander.pdf')
        extractor = Extractor(filepath=filepath)

        expected = '2013-02-19'
        self.assertEqual(expected, extractor.extract_due_date())

    def test_extract_due_date_with_zeros(self):
        filepath = '{}/{}'.format(self.assets_dir, 'santander.pdf')
        extractor = Extractor(filepath=filepath)
        extractor._barcode = '31890 00106 00114 285000 00202 067625 1 73600000042698'

        expected = '2017-12-01'
        self.assertEqual(expected, extractor.extract_due_date())

    def test_extract_all(self):
        filepath = '{}/{}'.format(self.assets_dir, 'santander.pdf')
        extractor = Extractor(filepath=filepath)

        expected = {
            'barcode': '03399 63290 64000 000006 00125 201020 4 56140000017832',
            'bank_code': '033',
            'bank': 'Banco Santander (Brasil) S.A.',
            'amount': 178.32,
            'due_date': '2013-02-19'
        }

        self.assertDictEqual(expected, extractor.extract_all())
