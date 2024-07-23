from odoo import models, fields, api

class StoreTransferLine(models.Model):
    _name = 'store.transfer.line'
    _description = 'Store Transfer Line'

    transfer_id = fields.Many2one('store.transfer', string='Store Transfer', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], default='draft', string='State')
