from odoo import http
from odoo.http import request
import json


class myMain(http.Controller):

    @http.route('/myhome', type='http', auth='user', website=True)
    def hello(self,**kwargs):
        print(kwargs)
        return request.render("website_custom.my_model_layout")

    @http.route('/myhome/submited', type='http', auth='user', method=['post'], website=True)
    def status(self,**kwargs):
        status = kwargs.get('status')
        if status == "success":
            return request.render("website_custom.my_model_status")