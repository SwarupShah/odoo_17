from odoo import fields, models,api,_
from odoo.exceptions import UserError


class SchoolTeacher(models.Model):
    _name = "provided.course.line"

    school_id = fields.Many2one('school.profile',string="school")
    course_id =  fields.Many2one('provided.course',string="Course Namem")
    total_student = fields.Integer(string="No. Student")

    @api.model_create_multi
    def create(self, vals_list):
        id =super().create(vals_list)
        student_result_obj = self.env['provided.course'].browse(id.course_id.id)
        new_number = student_result_obj.total_seats - id.total_student
        print(new_number)
        if new_number >= 0:
            student_result_obj.write({
                            'total_seats': new_number,
                        })
            return True
        else:
            raise ValueError("Quantity not available")
    
    def write(self, vals):
        if vals.values() in 'course_id':
            raise ValueError("You cannot changre course")
        else:
            student_result_obj = self.env['provided.course'].browse(self.course_id.id)
            new_number = self.total_student + student_result_obj.total_seats- vals['total_student']
            if new_number >= 0:
                student_result_obj.write({
                                'total_seats': new_number,
                            })
                return True
            else:
                raise ValueError("Quantity not available")
    
    def unlink(self):
        student_result_obj = self.env['provided.course'].browse(self.course_id.id)
        new_number = self.total_student + student_result_obj.total_seats
        student_result_obj.write({
                        'total_seats': new_number,
                    })
        super().unlink()
        return True