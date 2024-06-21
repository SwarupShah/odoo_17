/** @odoo-module **/

import { OrderWidget } from "@point_of_sale/app/generic_components/order_widget/order_widget";

export class qunatityAdd extends OrderWidget {
    // static template = "point_of_sale.QuantityAdded";
    // async willStart() {
    //     const result = await super.willStart();
    //     this.env.pos.on('change:selectedOrder', this, this._updateTotalQuantity);
    //     this._updateTotalQuantity();
    //     return result;
    // }
    // _updateTotalQuantity() {
    //     const currentOrder = this.env.pos.get_order();
    //     if (currentOrder) {
    //         const total_quantity = currentOrder.get_orderlines().reduce((sum, orderline) => {
    //             return sum + orderline.get_quantity();
    //         }, 0);
    //         this.state.total_quantity = total_quantity;
    //     }
    // }
    
}
