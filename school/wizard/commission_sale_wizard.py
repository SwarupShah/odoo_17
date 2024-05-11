from odoo import api, fields, models

class CommissionWizard(models.TransientModel):
    _name = 'commission.sale.wizard'
    _description = 'Commission Wizard'

    sales_person_id = fields.Many2one('res.users', string='Sales Person', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    def action_calculate_commission(self):
        print(self.sales_person_id)
        domain = [
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date),
            ('user_id', '=', self.sales_person_id.id),  
        ]            
        action = self.env.ref('school.action_sale_select_commission').read()[0]
        action['domain'] = domain
        action['view_mode'] = 'tree'
        return action
