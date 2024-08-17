from odoo import models, fields, api
import csv
import base64

class ConsolidatedData(models.Model):
    _name = 'consolidated.data'
    _description = 'Consolidated CSV Data'

    rut = fields.Char('RUT', required=True)
    csv_file_date = fields.Date('CSV File Date', required=True)
    csv_file_name = fields.Char('CSV File Name', required=True)
    document_id = fields.Many2one('documents.document', string='Document')
    sharing_url = fields.Char('Sharing URL')

    tipo_contribuyente_id = fields.Many2one('tipo.contribuyente', string='Tipo de Contribuyente')
    tipo_id = fields.Many2one('tipo', string='Tipo')
    activity_codes = fields.Many2many('activity.code', string='Giro Informado')

    @api.model
    def create_from_csv(self, csv_file, csv_file_date, csv_file_name):
        csv_data = base64.b64decode(csv_file)
        csv_lines = csv_data.decode('utf-8').splitlines()
        reader = csv.reader(csv_lines)

        rut = None
        record_data = {
            'csv_file_date': csv_file_date,
            'csv_file_name': csv_file_name,
            'activity_codes': [],
        }

        for row in reader:
            if row:
                field_name = row[0]
                field_value = row[1] if len(row) > 1 else None

                if field_name == 'RUT':
                    rut = field_value
                    record_data['rut'] = rut
                elif field_name == 'Tipo de contribuyente' and field_value:
                    tipo_contribuyente = self.env['tipo.contribuyente'].search([('name', '=', field_value)], limit=1)
                    if not tipo_contribuyente:
                        tipo_contribuyente = self.env['tipo.contribuyente'].create({
                            'name': field_value,
                        })
                    record_data['tipo_contribuyente_id'] = tipo_contribuyente.id
                elif field_name == 'Tipo' and field_value:
                    tipo = self.env['tipo'].search([('name', '=', field_value)], limit=1)
                    if not tipo:
                        tipo = self.env['tipo'].create({
                            'name': field_value,
                        })
                    record_data['tipo_id'] = tipo.id
                elif field_name == 'Giro informado' and field_value:
                    activities = field_value.split(',')
                    activity_codes = next(reader)[1].split(',') if len(row) > 1 else []
                    for activity, code in zip(activities, activity_codes):
                        if code:
                            activity_code = self.env['activity.code'].search([('code', '=', code)], limit=1)
                            if not activity_code:
                                activity_code = self.env['activity.code'].create({
                                    'code': code,
                                    'description': activity,
                                })
                            record_data['activity_codes'].append(activity_code.id)

        # Create the consolidated data record
        record = self.create(record_data)

        # Store the file in the Documents app
        attachment = self.env['ir.attachment'].create({
            'name': csv_file_name,
            'type': 'binary',
            'datas': csv_file,
            'mimetype': 'text/csv',
        })

        document = self.env['documents.document'].create({
            'name': csv_file_name,
            'attachment_id': attachment.id,
        })

        record.write({
            'document_id': document.id,
            'sharing_url': document.url,
        })
        
        return record
