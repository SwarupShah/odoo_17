from odoo import http
from odoo.http import request
import json
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal as pager



class myMain(http.Controller):

    @http.route('/myhome', type='http', auth='public', website=True)
    def hello(self,**kwargs):
        # sale_orders = request.env['sale.order'].sudo().search([])
        sale_order_line = None
        view_table = False
        error = False
        if kwargs.get('search_order'):
            # sale_order_line = request.env['sale.order'].browse(int(orderNames))
            sale_order_line = request.env['sale.order'].search([('name', 'ilike', kwargs.get('search_order'))])
            if len(sale_order_line.ids) == 0:
                error = True
            view_table = True
        return request.render("website_custom.my_model_layout", {
            # 'sale_orders': sale_orders,
            'sale_order_line': sale_order_line,
            'view_table': view_table,
            'error': error,
        })

    @http.route('/myhome/submited', type='http', auth='public', methods=['GET', 'POST'], website=True)
    def status(self, **kwargs):
        if request.httprequest.method == 'POST':
            try:
                if request.env.user.name == "Public user":
                    request.env['public.data'].create({
                        'email': kwargs.get('email'),
                        'password': kwargs.get('password'),
                    })
                else:
                    request.env['signed.data'].create({
                        'user_id': request.env.uid,
                        'email': kwargs.get('email'),
                        'password': kwargs.get('password'),
                    })
                return request.redirect('/myhome/submited?status=success')
            except Exception as e:
                return request.redirect('/myhome/submited?status=error')

        elif request.httprequest.method == 'GET':
            status = kwargs.get('status')
            if status == "success":
                return request.render("website_custom.my_model_status")
            elif status == "error":
                return request.render("website_custom.my_model_status")
            else:
                return request.redirect('/myhome')

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