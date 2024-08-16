from odoo import models, fields, api

class CrossoveredBudgetLines(models.Model):
    _inherit = 'crossovered.budget.lines'

    custom_theoritical_amount = fields.Float(compute='_compute_theoretical_amount')
    x_studio_monetary_field_6tn_1hwmk7pr = fields.Float(string="Disponible Ppto")  # Define the missing field

    @api.depends('custom_planned_amount', 'custom_practical_amount')
    def _compute_theoretical_amount(self):
        for record in self:
            plannedcstm = abs(record.custom_planned_amount or 0)
            practicalcstm = abs(record.custom_practical_amount or 0)
            if plannedcstm > practicalcstm:
                dispon = plannedcstm - practicalcstm
            else:
                dispon = 0
            record.custom_theoritical_amount = dispon
            record.x_studio_monetary_field_6tn_1hwmk7pr = dispon
