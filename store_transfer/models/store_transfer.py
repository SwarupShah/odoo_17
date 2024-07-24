from odoo import models, fields, api

class StoreTransfer(models.Model):
    _name = 'store.transfer'
    _description = 'Store Transfer'

    source_warehouse_id = fields.Many2one('stock.warehouse', string='Source Warehouse', required=True)
    destination_warehouse_id = fields.Many2one('stock.warehouse', string='Destination Warehouse', required=True)
    transfer_line_ids = fields.One2many('store.transfer.line', 'transfer_id', string='Transfer Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], default='draft', string='State', store=True)
    picking_ids = fields.One2many('stock.picking', 'transfer_id', string='Related Pickings', readonly=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')  # Added field to link to sale order
    picking_id_count = fields.Integer(string="Count Transfer", compute="_compute_transfer", store=True)

    @api.depends('picking_ids')
    def _compute_transfer(self):
        for transfer in self:
            transfer.picking_id_count = len(transfer.picking_ids)

    def action_store_transfer(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transfer',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('transfer_id', '=', self.id)],
            'context': {'create': False}
        }

    def approve_transfer(self):
        move_lines = []
        origin = self.env.context.get('order_name', '')
        for line in self.transfer_line_ids:
            move_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'location_id': self.source_warehouse_id.lot_stock_id.id,
                'location_dest_id': self.destination_warehouse_id.lot_stock_id.id,
                'name': line.product_id.name,
            }))

        picking = self.env['stock.picking'].create({
            'partner_id': self.destination_warehouse_id.partner_id.id,
            'picking_type_id': self.source_warehouse_id.out_type_id.id,
            'location_id': self.source_warehouse_id.lot_stock_id.id,
            'location_dest_id': self.destination_warehouse_id.lot_stock_id.id,
            'origin': origin if origin != "" else "Outgoing shipment to " + self.destination_warehouse_id.name + " from " + self.source_warehouse_id.name,
            'move_ids_without_package': move_lines,
            'transfer_id': self.id,
        })

        picking.action_confirm()
        self.picking_ids = [(4, picking.id)]
        self.state = 'confirmed'
