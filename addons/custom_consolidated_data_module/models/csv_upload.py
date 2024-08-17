from odoo import models, fields, api
import csv
import base64
from datetime import datetime

class CSVUpload(models.Model):
    _name = 'csv.upload'
    _description = 'CSV File Upload'

    name = fields.Char(string='File Name', readonly=True)
    file_data = fields.Binary(string='CSV File', required=True)
    file_name = fields.Char(string='CSV File Name')
    rut = fields.Char(string='RUT', readonly=True)
    file_creation_date = fields.Datetime(string='File Creation Date', readonly=True)
    extraction_date = fields.Datetime(string='CSV Data Extraction Date', readonly=True)
    unique_code = fields.Char(string='CSV Unique Code', readonly=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
        ('error', 'Error'),
    ], string='Status', default='draft')

    def action_analyze_csv(self):
        file_content = base64.b64decode(self.file_data)
        csv_data = csv.reader(file_content.decode().splitlines())

        # Extract basic fields from CSV
        first_row = next(csv_data)
        self.rut = first_row[0]  # Example: RUT might be the first field
        self.file_creation_date = datetime.now()  # Replace with actual extracted date if available
        self.extraction_date = datetime.now()
        self.unique_code = self.extract_unique_code(self.file_name)

        # Implement your validation logic here
        if self.is_duplicate():
            self.status = 'error'
            raise ValueError("Duplicate file detected!")
        
        self.status = 'validated'

    def extract_unique_code(self, file_name):
        if "reporte-" in file_name:
            return file_name.split("reporte-")[1].split(".csv")[0]
        return ''

    def is_duplicate(self):
        # Logic to check for duplicates
        existing_files = self.search([('unique_code', '=', self.unique_code), ('file_name', '=', self.file_name)])
        return bool(existing_files)
