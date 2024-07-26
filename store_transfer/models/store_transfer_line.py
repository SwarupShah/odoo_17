from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StoreTransferLine(models.Model):
    _name = 'store.transfer.line'
    _description = 'Store Transfer Line'

    transfer_id = fields.Many2one('store.transfer', string='Store Transfer', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)

    @api.constrains('quantity')
    def _check_quantity(self):
        for qty in self:
            if qty.quantity <= 0:
                raise ValidationError("Quantity must be greater than zero.")

    # @api.model
    # def _get_product(self):
    #     print("=============================")
    #     print("if")
    #     warehouse_id = self.transfer_id.source_warehouse_id.id
    #     products = self.env['product.product'].with_context(warehouse=warehouse_id).search([('qty_available', '>', 0)])
    #     print(products)
    #     product_ids = products.ids
    #     return product_ids
        #     # return {
        #     #     'domain': {'product_id': [('id', 'in', product_ids)]}
        #     # }
        # else:
        #     print("else")
        #     return []
        #     # return {
        #     #     'domain': {'product_id': []}
        #     # }
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.transfer_id.state == 'confirmed':
                move_line = [(0, 0, {
                    'product_id': record.product_id.id,
                    'product_uom_qty': record.quantity,
                    'location_id': record.transfer_id.source_warehouse_id.lot_stock_id.id,
                    'location_dest_id': record.transfer_id.destination_warehouse_id.lot_stock_id.id,
                    'name': record.product_id.name,
                })]
                record.transfer_id.create_picking('', move_line)
            elif record.transfer_id.state == 'cancel' or record.transfer_id.state == 'done':
                raise ValidationError("Cannot add lines to a canceled transfer.")
        return records