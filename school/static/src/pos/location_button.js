/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { TextAreaPopup } from "@point_of_sale/app/utils/input_popups/textarea_popup";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { CustomDroapdownPopup } from "@school/pos/custom_droapdown_popup"
import { onMounted, useRef, useState } from "@odoo/owl";

// import { Order } from "@point_of_sale/app/store/models";
// import { patch } from "@web/core/utils/patch";

export class OrderlocationButton extends Component {
    static template = "point_of_sale.locationButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
        this.orm = useService("orm");
        this.state = useState({ locationText: _t("Location") });

    }
    async showLorning(){
        await this.popup.add(ErrorPopup, {
            title: _t("Invalid Discount"),
            body: _t("You can't add a discount of %s%. Please enter a value between 0% and 100%.", values),
            cancelKey: true,
        });
    }
    async onClick() {
        const selectedOrderline = this.pos.get_order().get_selected_orderline();
        const order = this.pos.get_order();
       
        // console.log(this.pos)
        // FIXME POSREF can this happen? Shouldn't the orderline just be a prop?
        if (!selectedOrderline) {
            return;
        }
        const locations = await this.orm.call('pos.order', 'get_location', ['true']);
        // console.log(locations)
        const { confirmed, payload: selectedLocation } = await this.popup.add(CustomDroapdownPopup, {
            // startingValue: selectedOrderline.get_customer_note(),
            title: _t("Add Location"),
            locations: locations, 
        });
        if (confirmed) {
            if (selectedLocation == "Select Location"){
                this.showLorning()
            }
            else{
                this.state.locationText = selectedLocation || _t("Location");
                //i am able to get data here when i write anything in the popup
            }
        }
    }
}


ProductScreen.addControlButton({
    component: OrderlocationButton,
    // condition: function () {
    //     return this.pos.config.enable_school;
    // },
});

