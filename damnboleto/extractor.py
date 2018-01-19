import pdftotext
import re

from damnboleto.banks import bank_codes


class Extractor:
    """
    Class that read and extract a bunch of boleto's data.
    """

    def __init__(self, filepath: str, password=''):
        self.pdf = self._load_file(filepath=filepath, password=password)

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
    def _sanitize_boleto_number(cls, boleto_number: str) -> str:
        """
        Remove boleto's dots.
        Desired output: 00000 00000 00000 000000 00000 000000 0 00000000000000
        :param boleto_number: Extracted boleto's number
        :return: Sanitized boleto number
        """
        return boleto_number.replace('.', ' ')

    def extract_boleto_number(self) -> str:
        """
        Find and returns boleto's number from a PDF represented by str.
        :return: Boleto's number
        """
        boleto_number_pattern = r'\d{5}[\.|\s]{1}\d{5}\s\d{5}[\.|\s]{1}\d{6}\s\d{5}[\.|\s]{1}\d{6}\s\d\s\d{14}'
        regex = re.compile(pattern=boleto_number_pattern)

        for page in self.pdf:
            result = regex.search(page)
            if result:
                return self._sanitize_boleto_number(result.group())

    def extract_bank_code(self, boleto_number: str) -> str:
        """
        Extract bank code from boleto's number.
        Bank code is the first three digits.
        :param boleto_number: Extracted boleto's number
        :return: Bank code
        """
        return boleto_number[:3]

    def extract_bank(self, bank_code: str) -> str:
        """
        Find and returns bank related to extracted bank code.
        :param bank_code: Extracted bank code
        :return: Bank's name
        """
        return bank_codes.get(bank_code, 'Banco não encontrado.')

    def extract_all(self) -> dict:
        """
        Extract all data from boleto.
        :return: dict with all extracted data
        """
        boleto_number = self.extract_boleto_number()
        bank_code = self.extract_bank_code(boleto_number)
        return {
            'boleto_number': self.extract_boleto_number(),
            'bank_code': bank_code,
            'bank': self.extract_bank(bank_code),
        }
