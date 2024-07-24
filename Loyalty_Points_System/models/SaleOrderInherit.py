from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    points_earned = fields.Integer(string='Points Earned', compute='_compute_total_points_on_sale_order', store=True)
    points_redeemed = fields.Integer(string='Points Redeemed')
    discount_amount = fields.Monetary(string='Discount Amount')


    @api.depends('order_line.price_subtotal')
    def _compute_total_points_on_sale_order(self):
        # print(self.partner_id)
        # print(self.amount_total)
        credit_amount = 0
        credit_amount += self.amount_total
        self.points_earned = credit_amount / 10

    @api.onchange('points_redeemed')
    def redeem_points_from_loyalty_points(self):
          flag = 0
          if self.points_redeemed:
            if self.points_redeemed > self.amount_total:
                raise ValidationError("Redeemed points amount should not be more than total order amount")
            if not(self.partner_id):
              raise ValidationError("Please Select Customer Before Point Redemption")

            loyaltyObj = self.env['loyalty.points'].search([])
            # print(loyaltyObj)
            for cus in loyaltyObj:
                if cus.customer_id == self.partner_id:
                   flag = 1
                   if self.points_redeemed > cus.balance:
                       raise ValidationError('Customer has insufficient points')
                   else:
                       convert_discount = self.points_redeemed
                       self.discount_amount = convert_discount
            if flag == 0:
                raise ValidationError("You can't redeem points for this customer, because it is not in loyalty customer list")

    def create_new_loyalty_customer(self):
        res = self.env['loyalty.points'].create({
            'customer_id': self.partner_id.id,
            'points_earned': self.points_earned,
            'points_redeemed': 0,
            'balance': self.points_earned
        })
        return res

    def action_confirm(self):
        loyaltyObj = self.env['loyalty.points'].search([])
        flag = 0
        for cus in loyaltyObj:
            if cus.customer_id == self.partner_id:
                flag = 1
        if flag == 0:
            self.create_new_loyalty_customer()
            # pass
        for cus in loyaltyObj:
            if cus.customer_id == self.partner_id:
               cus.points_earned += self.points_earned
               cus.points_redeemed += self.points_redeemed
               self.amount_total -= self.discount_amount
               cus.balance -= self.points_redeemed
               cus.balance += self.points_earned
               break

        return super(SaleOrderInherit, self).action_confirm()






