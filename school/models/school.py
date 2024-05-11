from odoo import fields, models,api,_
from odoo.exceptions import UserError


class SchoolProfile(models.Model):
    _name = "school.profile"
    # _inherit = ['mai.thread']
    _description = "This is school profile."
    
    number = fields.Char(string='Teacher Reference ID', readonly=True, tracking=True, copy=False,
       default=lambda self: self.env['ir.sequence'].next_by_code(
           'class.teacher.reference'))
    name = fields.Char(string="School Name", required=True, help="Enter the name of the school")
    email = fields.Char(string="Email", help="Enter the email address of the school")
    phone = fields.Integer(string="Phone", help="Enter the phone number of the school")
    organisation = fields.Selection([("government", "Government"),("private", "Private")], string="Organisation", help="Select the type of organisation", default="private")
    student_ids = fields.One2many("school.student",'school_id', string="No. of student", readonly=True)
    teacher_ids = fields.One2many("school.teacher",'school_id', string="No. of teacher",readonly=True)
    class_ids = fields.One2many("school.class", "schools", string="Classes", readonly=True)
    student_count = fields.Integer(string="Student Count", compute="_compute_student_count")
    teacher_count = fields.Integer(string="Teacher Count", compute="_compute_teacher_count")
    class_count = fields.Integer(string="Class Count", compute="_compute_class_count")

    @api.depends('student_ids')
    def _compute_student_count(self):
        for school in self:
            school.student_count = len(school.student_ids)

    @api.depends('teacher_ids')
    def _compute_teacher_count(self):
        for school in self:
            school.teacher_count = len(school.teacher_ids)

    @api.depends('class_ids')
    def _compute_class_count(self):
        for school in self:
            school.class_count = len(school.class_ids)

    def action_get_student_record(self):
        # Check if the action is triggered from a form view and not in create mode
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'view_mode': 'tree,form',
            'res_model': 'school.student',
            'target':'new',
            'domain': [('school_id', '=', self.id)],
            'context': {'create': False}
        }

    def action_get_class_record(self):
        # Check if the action is triggered from a form view and not in create mode
        return {
            'type': 'ir.actions.act_window',
            'name': 'Class',
            'view_mode': 'tree,form',
            'res_model': 'school.class',
            'target':'new',
            'domain': [('schools', '=', self.id)],
            'context': {'create': False}
        }

    def action_get_teacher_record(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teachers',
            'view_mode': 'tree,form',
            'res_model': 'school.teacher',
            'target':'new',
            'domain': [('school_id', '=', self.id)],
            'context': {'create': False}
        }


    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the school model"""
        for vals in vals_list:
            if vals.get('number', _('New')) == _('New'):
                vals['number'] = self.env['ir.sequence'].next_by_code(
                    'school.profile')
        return super().create(vals_list)

    def unlink(self):
        return {
            'name': 'Delete School',
            'type': 'ir.actions.act_window',
            'res_model': 'cancel.school.wizard',
            'view_mode': 'form',
            'target': 'new'
        }

    def copy(self, default=None):
        raise UserError(_('You cannot duplicate the school recurds.'))
    
    def action_confirm(self):
        self.write({'organisation': 'government'})
    
    def browse_button(self):
        res = super().browse(self.id)
        print(res)
        
class OrderConfirmationButton(models.Model):
    _inherit = 'school.profile'

    def create_government(self):
        self.action_confirm()
        return True
