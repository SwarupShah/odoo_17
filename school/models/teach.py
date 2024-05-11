from odoo import fields, models,api,_
from odoo.exceptions import UserError


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "This is school teacher model."
    _inherit = "school.person"

    number = fields.Char(string='Teacher Reference ID', readonly=True,tracking=True, copy=False,
       default=lambda self: self.env['ir.sequence'].next_by_code(
           'class.teacher.reference'))
    join_date = fields.Date(string="Join Date", required=True, help="Enter the joining date of the teacher")
    salary = fields.Monetary(string="Salary", help="Enter the salary of the teacher")
    currency_id = fields.Many2one(comodel_name='res.currency',default=lambda self: self.env['res.currency'].search([('name', '=', 'INR')]).id,readonly=True)
    subject = fields.Many2one("school.subject", string="Subject", required=True, help="Select the subject of the teacher")
    school_id = fields.Many2one("school.profile", string="School", required=True, help="Select the school of the teacher")
    
    
    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the teacher model"""
        for vals in vals_list:
            if vals.get('number', _('New')) == _('New'):
                vals['number'] = self.env['ir.sequence'].next_by_code(
                    'school.teacher')
        return super().create(vals_list)