
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_studio_credito_ceec = fields.Monetary(string='CEEC 65%', compute='_compute_ceec_discount', store=True, currency_field='currency_id')

    @api.depends('order_line.price_subtotal', 'order_line.tax_id', 'order_line.product_id')
    def _compute_ceec_discount(self):
        for order in self:
            total_ceec_discount = 0  # Inicializar el descuento total

            for line in order.order_line:
                if any(tax.id == 884 for tax in line.tax_id):
                    product_code = line.product_id.default_code
                    if 'RMC' in product_code:
                        iva_amount = line.price_subtotal * 0.19
                        ceec_discount = iva_amount * 0.65
                        total_ceec_discount += ceec_discount

            order.x_studio_credito_ceec = -total_ceec_discount  # El valor es negativo para indicar un descuento
