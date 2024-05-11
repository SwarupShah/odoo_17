from odoo import fields, models, _, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


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
