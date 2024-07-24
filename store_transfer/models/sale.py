from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderSale(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[('store_transfers', "Store Transfers")],
    )

    def action_confirm(self):
        for order in self:
            product_qty_needed = {}

            for line in order.order_line:
                product_qty_available = line.product_id.with_context(warehouse='BVS').qty_available
                print("=====================", product_qty_available)

                if product_qty_available < line.product_uom_qty:
                    product_qty_needed[line.product_id] = line.product_uom_qty - product_qty_available

            if product_qty_needed:
                source_warehouse = self.env['stock.warehouse'].search([('code', '=', 'BVS')], limit=1)
                if not source_warehouse:
                    raise UserError('Insufficient stock and no other warehouses available.')

                transfer_lines = [(0, 0, {
                    'product_id': product.id,
                    'quantity': qty_needed
                }) for product, qty_needed in product_qty_needed.items()]

                transfer = self.env['store.transfer'].create({
                    'source_warehouse_id': source_warehouse.id,
                    'destination_warehouse_id': order.warehouse_id.id,
                    'transfer_line_ids': transfer_lines,
                    'sale_order_id': order.id  # Link the transfer to the sale order
                })

                order.state = 'store_transfers'
                context = {'order_name': order.name}
                transfer.with_context(context).approve_transfer()
                
                return True  # Skip the confirmation process for now

        # If no store transfers were needed, confirm the order as usual
        return super(SaleOrderSale, self).action_confirm()

    def action_view_shop(self):
        picking_ids = [x.id for x in self.picking_ids]
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transfer',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('id', 'in', picking_ids)],
            'context': {'create': False}
        }

