from odoo import fields, models,api,_
from odoo.exceptions import UserError


class SchoolProfile(models.Model):
    _name = "school.profile"
    # _inherit = ['mai.thread']
    _description = "This is school profile."
    
    number = fields.Char(string='Teacher Reference ID', readonly=True, copy=False,
       default=lambda self: self.env['ir.sequence'].next_by_code(
           'class.teacher.reference'))
    name = fields.Char(string="School Name", required=True, help="Enter the name of the school")
    email = fields.Char(string="Email", help="Enter the email address of the school")
    phone = fields.Integer(string="Phone", help="Enter the phone number of the school")
    organisation = fields.Selection([("government", "Government"),("private", "Private")], string="Organisation", help="Select the type of organisation", default="private")
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")

    student_ids = fields.One2many("school.student",'school_id', string="No. of student",readonly=True)
    teacher_ids = fields.One2many("school.teacher",'school_id', string="No. of teacher",readonly=True)
    class_ids = fields.One2many("school.class", "schools", string="Classes", readonly=True)
    course_ids = fields.One2many("provided.course.line","school_id",string="Courses")
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

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = f"{record.name} ({record.organisation})"
    #         result.append((record.id, name))
    #     return result

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

    # def unlink(self):
    #     return {
    #         'name': 'Delete School',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'cancel.school.wizard',
    #         'view_mode': 'form',
    #         'target': 'new'
    #     }

    def copy(self, default=None):
        raise UserError(_('You cannot duplicate the school recurds.'))
    
    def action_confirm(self):
        self.write({'organisation': 'government'})
    
    def browse_button(self):
        res = super().browse(self.id)
        print(res)
        # ras =  super().copy()
        # print(ras.name)
        # rps =  super().copy({
        #     'name':'rahul'
        # })
        # print(rps.name)
    
    def action_send_email(self):
        # template_id = self.env.ref('school.mail_template_blog')  # Replace 'your_module.email_template_id' with the actual ID of your email template
        # template_id.send_mail(self.id, force_send=True)
        self.ensure_one()
        # self.order_line._validate_analytic_distribution()
        lang = self.env.context.get('lang')
        mail_template = self.env.ref('school.mail_school_template_blog')
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'sale.order',
            'default_res_ids': self.ids,
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
        
    # def action_send_email(self):
    #     mail_template = self.env.ref(sale.mail_template_blog)
    #     mail_template.send_mail(self.id, force_send=True)
    
class OrderConfirmationButton(models.Model):
    _inherit = 'school.profile'

    def create_government(self):
        self.action_confirm()
        return True
