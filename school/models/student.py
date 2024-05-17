from odoo import fields, models,api,_

class SchoolStudent(models.Model):
    _inherit = "school.person"
    _name = "school.student"
    _description = "This is school Student model."
    

    number = fields.Char(string='Student Reference ID', readonly=True,tracking=True, copy=False,
       default=lambda self: self.env['ir.sequence'].next_by_code(
           'class.teacher.reference'))
    class_id = fields.Many2one('school.class', string="Class Room", help="Select the class of the student")
    subject_ids = fields.Many2many('school.subject', string="Subjects", help="Select the subjects of the student")
    enrollment_date = fields.Date(string="Enrollment Date", help="Enter the enrollment date of the student")
    school_id = fields.Many2one("school.profile", string="School", required=True, help="Select the school of the student")
    total_fee = fields.Float(string="Total Fee", help='Total Fee payed by the student', required=True,default=0)
    marks_ids = fields.One2many("student.mark", 'student_id', string="Student Marks")
    result_ids = fields.One2many("student.result","student_id",string="Results")
    student_data = fields.Selection([("removed", "Removed"),("available", "Available")], string="Result Available status", help="If field is showing removed than student result are removed or present", default="available")
    result_count = fields.Integer(string="Result count", compute="_compute_result_count")
    marks_count = fields.Integer(string="marks count", compute="_compute_marks_count")
    
    @api.depends('result_count')
    def _compute_result_count(self):
        for student in self:
            student.result_count = len(student.result_ids)

    @api.depends('marks_count')
    def _compute_marks_count(self):
        for student in self:
            student.marks_count = len(student.marks_ids)
            
    def action_get_marks_record(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stuent Marks',
            'view_mode': 'tree,form',
            'res_model': 'student.mark',
            'target':'new',
            'domain': [('student_id', '=', self.id)],
            'context': {'create': False}
        }

    def action_get_result_record(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stuent result',
            'view_mode': 'tree,form',
            'res_model': 'student.result',
            'target':'new',
            'domain': [('student_id', '=', self.id)],
            'context': {'create': False}
        }

    @api.model
    def create(self, vals):
        if vals.get('number', _('New')) == _('New'):
            vals['number'] = self.env['ir.sequence'].next_by_code('school.student')

        student = super(SchoolStudent, self).create(vals)

        student_result_obj = self.env['student.result']
        student_marks_obj = self.env['student.mark']

        # Create student result record
        student_result_obj.create({
            'student_id': student.id,
            'status': 'pending'
        })

        # Create student marks records for each newly created student
        for subject in student.subject_ids:
            student_marks_obj.create({
                'student_id': student.id,
                'subject_id': subject.id
            })

        return student


    
    def remove_student(self):
        # Delete associated student result records using email and phone
        emails = self.mapped('email')
        phones = self.mapped('phone')
        student_results = self.env['student.result'].search([('student_id.email', 'in', emails), ('student_id.phone', 'in', phones)])
        # student_results.ensure_one()
        # print("search outcomes",student_results)
        student_marks = self.env['student.mark'].search([('student_id.email', 'in', emails), ('student_id.phone', 'in', phones)])
        # search_count_print = self.env['student.mark'].search_count([('student_id.email', 'in', emails), ('student_id.phone', 'in', phones)])
        # print(search_count_print)
        # search_read_print = self.env['student.mark'].search_read([('student_id.email', 'in', emails), ('student_id.phone', 'in', phones)])
        # print(search_read_print)
        # print("search outcomes for marks",type(student_marks),student_marks)
        # print(student_marks.subject_id)
        # print(student_marks.marks_obtained)
        unlink_outcome=student_results.unlink()
        # print("unlink outcome",unlink_outcome)
        student_marks.unlink()
        return super(SchoolStudent, self).write({'student_data':'removed'})
    
    def unlink(self):
        self.remove_student()
        super().unlink()
        return True
    
    def add_taxes_action(self):
        
        # return self.env['ir.actions.act_window']._for_xml_id("school_student.action_student_wizard")
        
        # return {
        #     'name': 'Add Total Fees',
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'notify.remove.data.wizard',
        #     'view_mode': 'form',
        #     'target': 'new',
        # }
        return {
            'name': 'Add Total Fees',
            'type': 'ir.actions.act_window',
            'res_model': 'total.amount.tax.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
    def action_send_email(self):
        # template_id = self.env.ref('school.mail_template_blog')  # Replace 'your_module.email_template_id' with the actual ID of your email template
        # template_id.send_mail(self.id, force_send=True)
        self.ensure_one()
        # self.order_line._validate_analytic_distribution()
        lang = self.env.context.get('lang')
        mail_template = self.env.ref('school.mail_student_template_blog')
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'school.student',
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
        