from odoo import models, fields, api

class loyaltywizard(models.TransientModel):
    _name = 'loyalty.wizard'
    _description = "Manually add values to customer"

    customer_id = fields.Many2one('res.partner', string='Customer')
    points_earned = fields.Integer(string='Points Earned')
    points_redeemed = fields.Integer(string='Points Redeemed')
    balance = fields.Integer(string='Balance')
    reason = fields.Text(string='Reason')

    def save(self):
        get_customer_id = self.env.context.get('active_id')
        get_model = self.env['loyalty.points'].browse(get_customer_id)

        res = get_model.write({
            'customer_id': self.customer_id.id,
            'points_earned': self.points_earned,
            'points_redeemed': self.points_redeemed,
            'balance': self.balance
        })
        return res
