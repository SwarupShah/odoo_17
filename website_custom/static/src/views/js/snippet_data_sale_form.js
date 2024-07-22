/* @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.saleOrderFormSnippet = publicWidget.Widget.extend({
    selector: '.s_sale_form_snippet',

    /**
     * @override
     */
    start: function () {
        this._super.apply(this, arguments);
        this._loadOrders();
        this._bindEvents();
    },

    _bindEvents: function () {
        this.$('.o_select_sale_order').on('change', this._set_order_data.bind(this));
    },

    _loadOrders: async function () {
        try {
            const orders = await jsonrpc(
                '/myhome/sale_data_form',
            );
            const ordersContainer = this.el.querySelector('.o_select_sale_order');
            if (ordersContainer) {
                ordersContainer.innerHTML = '<option value="-1">Select order ........</option>' + orders.map(order => `<option value="${order.id}">${order.name}</option>`).join('');
            } else {
                console.error('Orders container not found.');
            }
        } catch (error) {
            console.error('Error loading orders:', error);
        }
    },
    _set_order_data: function () {
        const ordersContainer = this.el.querySelector('.o_select_sale_order');
        const selectedValue = ordersContainer.value;
        // const selectedText = ordersContainer.options[ordersContainer.selectedIndex].text;

        console.log("Selected Order ID:", selectedValue);
        // console.log("Selected Order Name:", selectedText);
        
        
            const orderDataShow = this.el.querySelector('.order_data_show');
            if (orderDataShow) {
                if (selectedValue != -1){
                    orderDataShow.innerHTML = `<p>Selected Order ID: ${selectedValue}</p>`;
                }
                else{
                    orderDataShow.innerHTML = `<p></p>`;
                }
            } else {
                console.error('Order data container not found.');
            }
        
    },
});

export default publicWidget.registry.saleOrderFormSnippet;
