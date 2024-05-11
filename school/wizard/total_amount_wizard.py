from odoo import fields, models, api, _


class NotifyRemoveData(models.TransientModel):
    _name = 'total.amount.tax.wizard'
    _description = "This is a notification before removing student records."

    annual_fees = fields.Float(string="Annual Fees", help='Annual Fees Field', default=0)
    tuition_fees = fields.Float(string="Tuition Fees",help="Tuition Fees Field", default=0)
    admission_fees = fields.Float(string="Admission Fees",help="Admission Fees Field", default=0)
    transportation_fee = fields.Float(string="Transportation Fees",help="Transportation Fees Field", default=0)
    examination_fees = fields.Float(string="Examination Fees", help='Examination Fees Field',required=True, default=0)
    development_fees = fields.Float(string="Development Fees",help='Development Fees field', default =0)
    miscellaneous_fees = fields.Float(string="Miscellaneous Fees",help="Miscellaneous Fees Field", default = 0)
    other_fees = fields.Float(string="Other Fees",help="Other Fees Field", default = 0)

    # @api.model
    def add_total_amount_actions(self):
        # Calculate total fee
        total_fee = self.annual_fees + self.tuition_fees + self.admission_fees + \
                    self.transportation_fee + self.examination_fees + \
                    self.development_fees + self.miscellaneous_fees + self.other_fees

        # Update the total_fee field of the current student record
        active_student_id = self.env.context.get('active_id')
        if active_student_id:
            student = self.env['school.student'].browse(active_student_id)
            student.write({'total_fee': total_fee})

        # Close the wizard
        return {'type': 'ir.actions.act_window_close'}
