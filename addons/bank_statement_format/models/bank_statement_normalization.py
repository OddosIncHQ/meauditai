import base64
import io
import pdfplumber
import pandas as pd
import csv
import ofxparse
from ofxparse import OfxParser
import xml.etree.ElementTree as ET
from odoo import models, fields, api
from odoo.exceptions import UserError

class BankStatementNormalization(models.Model):
    _name = 'bank.statement.normalization'
    _description = 'Bank Statement Normalization'

    name = fields.Char(string='Name', required=True)
    file_type = fields.Selection([
        ('pdf', 'PDF'),
        ('xlsx', 'Excel'),
        ('csv', 'CSV'),
        ('ofx', 'OFX'),
        ('camt', 'CAMT'),
        ('qif', 'QIF')
    ], string='File Type', required=True, default='pdf')
    file = fields.Binary(string='Statement File', required=True)
    bank_name = fields.Selection([
        ('santander', 'Santander'),
        ('consorcio', 'Consorcio'),
        ('bbva', 'BBVA'),
        ('bci', 'BCI'),
    ], string='Bank Name', required=True)
    qif_separator = fields.Char(string='QIF Separator', default='\n')
    processed_data = fields.Binary(string='Processed Data', readonly=True)

    def process_statement(self):
        self.ensure_one()
        file_content = base64.b64decode(self.file)

        if self.file_type == 'pdf':
            transactions = self._process_pdf(file_content, self.bank_name)
        elif self.file_type == 'xlsx':
            transactions = self._process_xlsx(file_content, self.bank_name)
        elif self.file_type == 'csv':
            transactions = self._process_csv(file_content, self.bank_name)
        elif self.file_type == 'ofx':
            transactions = self._process_ofx(file_content, self.bank_name)
        elif self.file_type == 'camt':
            transactions = self._process_camt(file_content, self.bank_name)
        elif self.file_type == 'qif':
            transactions = self._process_qif(file_content, self.bank_name, self.qif_separator)
        else:
            raise UserError("Unsupported file type!")

        df = pd.DataFrame(transactions)
        output = io.BytesIO()
        df.to_excel(output, index=False)
        self.processed_data = base64.b64encode(output.getvalue())

    def _process_pdf(self, file_content, bank_name):
        transactions = []
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                lines = text.split('\n')
                transactions.extend(self._process_lines(lines, bank_name))
        return transactions

    def _process_xlsx(self, file_content, bank_name):
        transactions = []
        file_stream = io.BytesIO(file_content)
        df = pd.read_excel(file_stream)
        for index, row in df.iterrows():
            lines = [str(row[column]) for column in df.columns]
            transactions.extend(self._process_lines(lines, bank_name))
        return transactions

    def _process_csv(self, file_content, bank_name):
        transactions = []
        file_stream = io.StringIO(file_content.decode('utf-8'))
        reader = csv.reader(file_stream)
        for row in reader:
            lines = [str(cell) for cell in row]
            transactions.extend(self._process_lines(lines, bank_name))
        return transactions

    def _process_ofx(self, file_content, bank_name):
        transactions = []
        ofx = OfxParser.parse(io.BytesIO(file_content))
        for transaction in ofx.account.statement.transactions:
            lines = [
                transaction.date.strftime('%Y-%m-%d'),
                transaction.payee,
                str(transaction.amount)
            ]
            transactions.extend(self._process_lines(lines, bank_name))
        return transactions

    def _process_camt(self, file_content, bank_name):
        transactions = []
        root = ET.fromstring(file_content)
        for entry in root.findall('.//Ntry'):
            date = entry.find('.//BookgDt/Dt').text
            amount = entry.find('.//Amt').text
            detail = entry.find('.//RmtInf/Ustrd').text if entry.find('.//RmtInf/Ustrd') is not None else ''
            lines = [date, detail, amount]
            transactions.extend(self._process_lines(lines, bank_name))
        return transactions

    def _process_qif(self, file_content, bank_name, separator):
        transactions = []
        file_stream = io.StringIO(file_content.decode('utf-8'))
        current_transaction = {}
        for line in file_stream.read().split(separator):
            if line.startswith('D'):
                current_transaction['Date'] = line[1:].strip()
            elif line.startswith('T'):
                current_transaction['Amount'] = line[1:].strip()
            elif line.startswith('P'):
                current_transaction['Detail'] = line[1:].strip()
            elif line.startswith('^'):
                if current_transaction:
                    lines = [
                        current_transaction.get('Date'),
                        current_transaction.get('Detail'),
                        current_transaction.get('Amount')
                    ]
                    transactions.extend(self._process_lines(lines, bank_name))
                    current_transaction = {}
        return transactions

    def _process_lines(self, lines, bank_name):
        transactions = []
        if bank_name == 'santander':
            transactions.extend(self._process_santander(lines))
        elif bank_name == 'consorcio':
            transactions.extend(self._process_consorcio(lines))
        elif bank_name == 'bbva':
            transactions.extend(self._process_bbva(lines))
        elif bank_name == 'bci':
            transactions.extend(self._process_bci(lines))
        return transactions

    # Existing methods for processing specific banks (e.g., _process_santander, etc.) remain unchanged.
    # Ensure these methods are designed to work with lines from all supported file formats.