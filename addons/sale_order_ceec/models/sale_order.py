from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Define the CEEC Discount field
    x_studio_credito_ceec = fields.Monetary(
        string='CEEC 65%',
        compute='_compute_ceec_discount',
        store=True,
        currency_field='currency_id'
    )

    @api.depends('order_line.price_subtotal', 'order_line.tax_id', 'order_line.product_id')
    def _compute_ceec_discount(self):
        for order in self:
            total_ceec_discount = 0  # Initialize the total CEEC discount

            for line in order.order_line:
                # Check if the line has the specific tax (tax ID 884)
                if any(tax.id == 884 for tax in line.tax_id):
                    product_code = line.product_id.default_code
                    # Check if the product code contains 'RMC'
                    if 'RMC' in product_code:
                        # Calculate the IVA amount (19% of subtotal)
                        iva_amount = line.price_subtotal * 0.19
                        # Calculate the CEEC discount as 65% of the IVA amount
                        ceec_discount = iva_amount * 0.65
                        # Accumulate the CEEC discount
                        total_ceec_discount += ceec_discount

            # Set the total discount value (negative to represent a discount)
            order.x_studio_credito_ceec = -total_ceec_discount
