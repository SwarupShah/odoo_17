from odoo import api, fields, models

class BookOrderLine(models.Model):
    """ For managing order lines of booked order """
    _name = "school.order.line"
    _description = "Lines of school Booked Order"
    _rec_name = "product_id"

    company_id = fields.Many2one('res.company', string='Company',
                                 help="Company of the booked order",
                                 default=lambda self: self.env.user.company_id)
    product_id = fields.Many2one('product.product',
                                 help="Select products for ordering",
                                 string='Product',
                                 domain=[('sale_ok', '=', True)],
                                 required=True, change_default=True)
    price_unit = fields.Float(string='Unit Price',
                              help="Unite price of selected product", digits=0)
    qty = fields.Float(string='Quantity', default=1,
                       help="Enter how much quantity of product want ")
    price_subtotal = fields.Float(compute='_compute_amount_line_all',
                                  digits=0,
                                  help="Sub total amount of each order line"
                                       "without tax",
                                  string='Subtotal w/o Tax')
    price_subtotal_incl = fields.Float(compute='_compute_amount_line_all',
                                       digits=0, string='Subtotal',
                                       help="Sub total amount of each order "
                                            "line with tax")
    discount = fields.Float(string='Discount (%)', digits=0, default=0.0,
                            help="You can apply discount for each product")
    order_id = fields.Many2one('school.order', string='Order Ref',
                               help="Relation to book order field",
                               ondelete='cascade')
    # tax_ids = fields.Many2many('account.tax', string='Taxes',
    #                            readonly=True, help="Taxes for each line")
    # tax_after_fiscal_position_ids = fields.Many2many(
    #     'account.tax', 'account_tax_rel', 'uid',
    #     'tag_id', string='Taxes', help="Fiscal position after entering "
    #                                    "the tax")