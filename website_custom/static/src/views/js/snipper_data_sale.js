/* @odoo-module */  
import publicWidget from "@web/legacy/js/public/public_widget";
import { useService } from "@web/core/utils/hooks";

publicWidget.registry.s_sale_order_snippet = publicWidget.Widget.extend({
    selector: '.s_sale_order_snippet',
    
    start: function () {
        this._super.apply(this,arguments);
        this._bindEvents();
        this.rpc = useService("rpc");
        const attachment = this.rpc('/myhome/sale_data', {
            params: {},
        });
        this.passwordInput = document.querySelector(".orders") = attachment;
    },

});

export default publicWidget.registry.s_sale_order_snippet;