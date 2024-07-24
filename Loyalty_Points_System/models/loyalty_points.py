from odoo import models, fields, api

class LoyalityPoints(models.Model):
    _name = 'loyalty.points'
    _description = "Custom Loyalty Points"

    customer_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    points_earned = fields.Integer(string='Points Earned', readonly=True)
    points_redeemed = fields.Integer(string='Points Redeemed', readonly=True)
    balance = fields.Integer(string='Balance', readonly=True)




    def open_customer_loyalty_wizard(self):
        return {
            'name': 'Add info',
            'type': 'ir.actions.act_window',
            'res_model': 'loyalty.wizard',
            'view_mode': 'form',
            'target': 'new'
        }

    def action_generate_report(self):
       data = self.env['sale.order'].search([('partner_id', '=', self.customer_id.id)])
       return self.env.ref('Loyalty_Points_System.loyalty_points_report').report_action(data)









