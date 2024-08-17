from odoo import models, fields

class ActivityCode(models.Model):
    _name = 'activity.code'
    _description = 'Activity Code'

    code = fields.Char('Code', required=True)
    description = fields.Text('Description')
