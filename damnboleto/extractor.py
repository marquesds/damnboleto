import pdftotext
import re

from damnboleto.constants import bank_codes
from datetime import datetime, timedelta

from damnboleto.exceptions import BarcodeNotFound


class Extractor:
    """
    Class that read and extract a bunch of boleto's data.
    """

    def __init__(self, filepath: str, password=''):
        self.pdf = self._load_file(filepath=filepath, password=password)
        self._barcode = self.extract_barcode()

    @classmethod
    def _load_file(cls, filepath: str, password: str) -> pdftotext.PDF:
        """
        Read a pdf file and extract its content into a pdftotext.PDF instance
        :param filepath: PDF's path
        :param password: PDF's password
        :return: pdftotext.PDF instance
        """
        with open(filepath, 'rb') as f:
            return pdftotext.PDF(f, password)

    @classmethod
    def _sanitize_barcode(cls, barcode: str) -> str:
        """
        Remove boleto's dots.
        Desired output: 00000 00000 00000 000000 00000 000000 0 00000000000000
        :param barcode: Extracted boleto's number
        :return: Sanitized boleto number
        """
        return barcode.replace('.', ' ')

    def extract_barcode(self) -> str:
        """
        Find and returns boleto's number from a PDF represented by str.
        :return: Boleto's number
        """
        barcode_pattern = r'\d{5}[\.|\s]{1}\d{5}\s\d{5}[\.|\s]{1}\d{6}\s\d{5}[\.|\s]{1}\d{6}\s\d\s\d{14}'
        regex = re.compile(pattern=barcode_pattern)

        for page in self.pdf:
            result = regex.search(page)
            if result:
                return self._sanitize_barcode(result.group())
        else:
            raise BarcodeNotFound('Could not find any valid barcode in document.')

    def extract_bank_code(self) -> str:
        """
        Extract bank code from boleto's number.
        Bank code is the first three digits.
        :return: Bank code
        """
        return self._barcode[:3]

    def extract_bank(self) -> str:
        """
        Find and returns bank related to extracted bank code.
        :return: Bank's name
        """
        return bank_codes.get(self._barcode[:3], 'Banco não encontrado.')

    def extract_amount(self) -> float:
        """
        Return boleto's total amount to be paid.
        :return: Total amount
        """
        last_section = self._barcode.split(' ')[-1]
        amount = int(last_section[4:]) / 100
        return amount

    def extract_due_date(self, date_format='%Y-%m-%d') -> str:
        """
        Calculate boleto's due date.
        :return: Sum of base date plus due date factor days
        """
        base_date = datetime(1997, 10, 7)  # acoording to http://bit.ly/2Djnh8B
        due_date_factor = self._barcode.split(' ')[-1]
        due_date_factor = int(due_date_factor[:4])
        return (base_date + timedelta(days=due_date_factor)).strftime(date_format)

    def extract_all(self) -> dict:
        """
        Extract all data from boleto.
        :return: dict with all extracted data
        """
        return {
            'barcode': self._barcode,
            'bank_code': self.extract_bank_code(),
            'bank': self.extract_bank(),
            'amount': self.extract_amount(),
            'due_date': self.extract_due_date()
        }
