from odoo import fields, models, _, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.exceptions import AccessError
from datetime import datetime, timedelta
import base64

class SaleOrder(models.Model):
    _inherit = "sale.order"

    checking_date = fields.Date(
        string="Ordering Date", help="enter the date when order was placed")

    nick_name = fields.Char(string="Nick Name")
    commission = fields.Float(
        string="Commission", compute="compute_commision_amount")

    # @api.depends("amount_total")
    # def compute_commision_amount(self):
    #     for i in self:
    #         if i.total_amount > i.partner_id.commission_amount_on:
    #             i.commission = (i.total_amount*i.partner_id.percentage)/100
    #         else:
    #             i.commission = sum(order.commission for order in record.order_ids)

    commission_order_id = fields.Many2one(
        'commission.order', string='Commission Order', readonly=True)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        commission_value =0.0
        if self.amount_total > self.user_id.partner_id.commission_amount_on:
            # print("partner_id.commission_amount_on",self.user_id.partner_id.commission_amount_on)
            commission_value = (self.amount_total*self.user_id.partner_id.percentage)/100
            
        if self.commission_order_id:
            self.commission_order_id.write({
                'order_id': self.name,
                'customer_name': self.user_id.name,
                'order_date': self.date_order,
                'commission': commission_value,
                'total': self.amount_total,
            })
        else:
            commission_order = self.env['commission.order'].create({
                'order_id': self.name,
                'customer_name': self.user_id.name,
                'order_date': self.date_order,
                'commission': commission_value,
                'total': self.amount_total,
            })
            self.commission_order_id = commission_order.id
        
        mail_template = self.env.ref('school.mail_order_comfirm_blog')
        mail_template.send_mail(self.id, force_send=True)
        return res

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        if self.commission_order_id:
            self.commission_order_id.unlink()
        return res

    @api.model
    def _get_order_lines_to_report(self):
        order_lines_context = self.env.context.get('order_lines')
        if order_lines_context:
            return self.order_line.filtered(lambda l: l.id in order_lines_context)
        return super(SaleOrder, self)._get_order_lines_to_report()

    def add_download_report_action(self):
        return {
            'name': 'Download Report',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.report.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id}
        }
        

    def run_monthly_notification(self):
        today = fields.Date.today()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

        # Now you have the starting and ending dates of the previous month
        start_date = first_day_of_previous_month
        end_date = last_day_of_previous_month
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", start_date, end_date)
        report_record = self.env['commission.sale.wizard']
        print(self.env.user.id)
        report_data, status = report_record.fetch_from_sale(start_date, end_date)
        if status:
            # Create the attachment
            attachment = self.env['ir.attachment'].create({
                'name': f'monthly_report_from_{start_date}_to_{end_date}.xlsx',
                'type': 'binary',
                'datas': base64.b64encode(report_data),
                'res_model': 'sale.order',
                'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            })

            action = self.env['res.users'].search([])
            for ras in action:
                # print(action)
                # Prepare email values for all records
                email_values = {
                    'email_from':f'{self.env.user.email}',
                    'email_to': f'{ras.login}',
                    'subject': f"Report from {start_date} to {end_date}",
                    'attachment_ids': [(6, 0, [attachment.id])]
                    # 'email_cc':['durgavao@mail.com','harshtandel@mail.com','janvibhadja@mail.com','dhatrimodhvadaya@mail.com']
                }

                # Send a single email with the report attachment to all recipients
                mail_template = self.env.ref('school.mail_monthly_report_template_blog')
                mail_template.send_mail(self.env.user.id, email_values=email_values, force_send=True)
        else:
            raise AccessError(_("OOPS! Unable to get record."))


        
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    nick_name = fields.Char(
        string="Nick Name", readonly=True, related='sale_id.nick_name')

    def add_download_report_action_delivery(self):
        return {
            'name': 'Download Delivery Report',
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.report.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id}
        }


class SaleOrderLines(models.Model):
    _inherit = "sale.order.line"

    # order_line_wiz = fields.Many2many(
    #     'sale.report.wizard', string="Orders")
    extra_tags = fields.Char(string="Extra field",
                             help="enter the date when order was placed")
    is_available = fields.Boolean(
        string="Is Available", compute="_compute_available_or_not", invisible=True)

    def _prepare_procurement_values(self, group_id=False):
        values = super(
            SaleOrderLines, self)._prepare_procurement_values(group_id)
        values.update({
            'extra_tags': self.extra_tags
        })
        return values

    # @api.depends('product_uom_qty', 'order_id.partner_id')
    # def _compute_available_or_not(self):
    #     for rec in self:
    #         product = rec.product_id
    #         print('>>>>>>>>>>>>>>>>>>>>>>p',product)
    #         if product:
    #             product_tmpl_id = product.product_tmpl_id
    #             print('>>>>>>>>>>>>>>>>>>>ptid',product_tmpl_id)
    #             virtual_available = self.env['product.template'].browse(product_tmpl_id.id).virtual_available
    #             rec.is_available = rec.product_uom_qty <= virtual_available
    #         else:
    #             rec.is_available = False


class writeAnotherDetail(models.Model):
    _inherit = "stock.move"

    extra_tags = fields.Char(string="Extra field",
                             help="enter the date when order was placed")


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['extra_tags']
        return fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    commission_amount_on = fields.Float(string='Commission Amount On')
    percentage = fields.Float(string="Percentage")
    b_date = fields.Date(
        string='Birthday date'
    )
    

    def action_send_email(self):
        self.ensure_one()
        # self.order_line._validate_analytic_distribution()
        lang = self.env.context.get('lang')
        mail_template = self.env.ref('school.mail_res_partner_template_blog')
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'res.partner',
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

    def run_bday_notification(self):
        today = fields.Date.today()
        today_month_day = today.strftime('%m-%d')  # Get the month and day in 'MM-DD' format

        records = self.search([])  # Get all records
        for rec in records:
            if rec.b_date and rec.b_date.strftime('%m-%d') == today_month_day:  # Compare month and day
                email_values = {
                    'email_to': rec.email,
                    'subject': f"Happy Birthday {rec.name}"
                }
                # print(f"Happy Birthday {rec.display_name}")
                mail_template = self.env.ref('school.mail_res_partner_template_blog')
                mail_template.send_mail(rec.id, email_values=email_values, force_send=True)
                # print(f"Happy Birthday {rec.display_name} Again")
    