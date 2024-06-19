/** @odoo-module **/
// import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
// import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

export class CreateButton extends Component {
	
    static template = "point_of_sale.CreateButton";
        
    /** 
    * Setup function to initialize the component.
    
    */
        
    setup() {    
    this.pos = usePos();
    this.numberBuffer = useService("number_buffer")
        
    // this.popup = useService("popup");
        
    }
	
    /** 
    * Click event handler for the create button.
    
    */
   get currentOrder() {
        return this.pos.get_order();
   }
    async onClick() {    
        const selectedOrderline = this.pos.get_order().get_selected_orderline();
        console.log("selectedOrderline",selectedOrderline);
        // var currentOrder = this.pos.get_order().get_partner()
        const selectedLine = this.currentOrder.get_selected_orderline();
        console.log("selectedLine",selectedLine)

        if (!selectedOrderline) {
            return;
        }
        this.currentOrder.removeOrderline(selectedLine);

        // this.popup.add(ErrorPopup, {
        //     title: _t("Cannot modify a tip"),
        //     body: _t("Customer tips, cannot be modified directly"),
        // });
        // console.log("frughug");
        
    }
}
/**
 * Add the OrderlineProductCreateButton component to the control buttons in
   the ProductScreen.
 */
ProductScreen.addControlButton({
    component: CreateButton,
    position: ["before","CustomerButton"]
});