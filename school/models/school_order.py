from odoo import api, fields, models

class SchoolOrder(models.Model):
    _name = 'school.order'
    _discription = 'school product order'

    name = fields.Char(string='Booking Ref', readonly=True, copy=False, default='/')   # ir sequence

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)

    date_order = fields.Date(string='Order Date', default=fields.Date.today())

    amount_total = fields.Float(string='Total', digits=0)

    note = fields.Text(string='Note')

    delivery_address = fields.Char(string='Delivery Address')

    delivery_date = fields.Date(string='Delivery Date')

    # school order line
    order_line_ids  = fields.One2many('school.order.line','order_id',string='Order Lines',)