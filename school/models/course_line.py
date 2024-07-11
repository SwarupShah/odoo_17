from odoo import fields, models,api,_
from odoo.exceptions import ValidationError
import pdb

class ProvidedCourseLine(models.Model):
    _name = "provided.course.line"
    _description = "This is course line teacher model."

    school_id = fields.Many2one('school.profile',string="school")
    course_id =  fields.Many2one('provided.course',string="Course Namem")
    total_student = fields.Integer(string="No. Student")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            
            id =super().create(vals)

            course_obj = self.env['provided.course'].browse(id.course_id.id)
            new_number = course_obj.total_seats - id.total_student
            print(new_number)
            if new_number >= 0:
                course_obj.write({
                                'total_seats': new_number,
                            })
            else:
                raise ValueError(_(f"For {course_obj.name} only {course_obj.total_seats} available"))
        return True
    
    def write(self, vals):
        if vals.values() in ['course_id']:
            raise ValueError(_("You cannot changre course"))
        else:
            student_result_obj = self.env['provided.course'].browse(self.course_id.id)
            new_number = self.total_student + student_result_obj.total_seats- vals['total_student']
            pdb.set_trace()
            if new_number >= 0:
                student_result_obj.write({
                                'total_seats': new_number,
                            })
                super().write(vals)
                return True
            else:
                raise ValueError(_("Quantity not available"))

    def unlink(self):
        for vals in self:
            student_result_obj = self.env['provided.course'].browse(vals.course_id.id)
            new_number = vals.total_student + student_result_obj.total_seats
            student_result_obj.write(
                {'total_seats': new_number}
                )
        result = super(ProvidedCourseLine, self).unlink()
        print(result)
        return result