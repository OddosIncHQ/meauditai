from odoo import models, fields, api
import base64
import pandas as pd
from io import BytesIO

class BankStatementImportWizard(models.TransientModel):
    _name = 'bank.statement.import.wizard'
    _description = 'Import Bank Statement from Excel'

    file_data = fields.Binary(string="Excel File", required=True)
    file_name = fields.Char(string="File Name")

    def import_bank_statement(self):
        # Decode file and load data
        file_content = base64.b64decode(self.file_data)
        file_data = BytesIO(file_content)
        
        # Read the Excel file using pandas
        df = pd.read_excel(file_data)

        # Mapping the columns based on the Python code provided
        transactions = []
        for _, row in df.iterrows():
            transaction = {
                'Fecha': row['Fecha'],
                'Descripcion': row['Descripcion'],
                'Documento': row.get('N° Documento', ''),
                'Cargos': row.get('Cargos', 0),
                'Abonos': row.get('Abonos', 0),
                'Saldo': row['Saldo']
            }
            transactions.append(transaction)

        # Import each transaction into the `bank.statement.processor`
        bank_statement = self.env['bank.statement.processor'].create({
            'name': self.file_name,
            'extracted_data': str(transactions)
        })

        # Redirect to the newly created record
        return {
            'type': 'ir.actions.act_window',
            'name': 'Imported Bank Statement',
            'res_model': 'bank.statement.processor',
            'view_mode': 'form',
            'res_id': bank_statement.id,
            'target': 'current',
        }
