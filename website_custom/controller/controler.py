from odoo import http
from odoo.http import request
import json
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal as pager



class myMain(http.Controller):

    @http.route('/myhome', type='http', auth='public', website=True)
    def hello(self,**kwargs):
        # print(kwargs)
        return request.render("website_custom.my_model_layout")

    @http.route('/myhome/submited', type='http', auth='public', method=['post'], website=True)
    def status(self,**kwargs):
        print(kwargs)
        status = kwargs.get('status')
        print(request.env.uid)
        if status == "success":
            if request.env.user.name == "Public user":
                request.env['public.data'].create({
                    'email': kwargs.get('email'),
                    'password': kwargs.get('password'),
                })
                return request.render("website_custom.my_model_status")
            else:
                request.env['signed.data'].create({
                    'user_id': request.env.uid,
                    'email': kwargs.get('email'),
                    'password': kwargs.get('password'),
                })
                return request.render("website_custom.my_model_status")


    @http.route('/saleOrder', type='http', auth='user', website=True)
    def saleOrders(self, **kwargs):
        order_data = request.env['sale.order'].search([('create_uid','=',request.env.uid),('access_token','!=',False)])
        print(order_data)
        return request.render("website_custom.shopping_customer_id", {
            'orders': order_data
        })
    
    @http.route('/saleOrder/<model("sale.order"):order>', type='http', auth='user', website=True)
    def saleOrder(self, order, access_token=None, **kwargs):
        if order.create_uid.id == request.env.uid:
            if order.access_token ==access_token:
                return request.render("website_custom.order_details", {
                    'order': order
                })
            else:
                return request.redirect('/saleOrder')
        else:
            return request.redirect('/saleOrder')