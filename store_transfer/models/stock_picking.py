from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # _logger = logging.getLogger(__name__)


    transfer_id = fields.Many2one("store.transfer", string="Stock Transfer")



    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if self.transfer_id:
            self.transfer_id.state = 'done'
            if self.transfer_id.sale_order_id:
                sale_order = self.transfer_id.sale_order_id
                # _logger.info(f"Archiving sale order: {sale_order.id}")
                print(sale_order.id)
                if sale_order:
                    print(sale_order)
                    # sale_order.state = 'draft'

                    sale_order.state= 'sale'
                    # self =sale_order
                    # orders = self.env['sale.order'].browse(sale_order.id).action_confirm()
                    # sale_order.action_confirm()
                else:
                    raise UserError("Sale order not found!")
        return res

            
    
