from odoo import models, fields, api

class StoreTransfer(models.Model):
    _name = 'store.transfer'
    _description = 'Store Transfer'

    source_warehouse_id = fields.Many2one('stock.warehouse', string='Source Warehouse', required=True)
    destination_warehouse_id = fields.Many2one('stock.warehouse', string='Destination Warehouse', required=True)
    transfer_line_ids = fields.One2many('store.transfer.line', 'transfer_id', string='Transfer Lines')
    # order_id = fields.Many2one()
    

    def approve_transfer(self):
        print(self.source_warehouse_id.lot_stock_id)
        # picking = self.env['stock.picking'].search([('origin','=',self.name)])
        move_lines = []
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
            'origin': "Outgoing shipment to " + self.destination_warehouse_id.name + " from " + self.source_warehouse_id.name,
            'move_ids_without_package': move_lines
        })