from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderSale(models.Model):

    _inherit = 'sale.order'

    def action_confirm(self):
        super(SaleOrderSale, self).action_confirm()
        for order in self:
            for line in order.order_line:
                product_qty_available = line.product_id.with_context(warehouse=order.warehouse_id.id).qty_available
                print("=====================",product_qty_available)
                if product_qty_available < line.product_uom_qty:
                    source_warehouse = self.env['stock.warehouse'].search([('id', '!=', order.warehouse_id.id)], limit=1)
                    if not source_warehouse:
                        raise UserError('Insufficient stock and no other warehouses available.')
                    
                    transfer = self.env['store.transfer'].create({
                        'source_warehouse_id': source_warehouse.id,
                        'destination_warehouse_id': order.warehouse_id.id,
                        'transfer_line_ids': [(0, 0, {
                            'product_id': line.product_id.id,
                            'quantity': line.product_uom_qty,
                        })]
                    })
                    order.warehouse_id = source_warehouse.id
                    print(transfer)
                    # transfer._action_confirm()
                    # transfer.action_done()
                    # Adjust stock in sales order's warehouse
                    line.product_id.with_context(warehouse=order.warehouse_id.id).qty_available += line.product_uom_qty