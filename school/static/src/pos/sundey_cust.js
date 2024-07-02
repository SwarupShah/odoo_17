/**@odoo-module **/

import { PartnerListScreen } from "@point_of_sale/app/screens/partner_list/partner_list";
// import { usePos } from "@point_of_sale/app/store/pos_hook";
// import { CustomAlertPopup } from "@pos_buttons/js/PopUp/pos_pop_up";
import { patch } from "@web/core/utils/patch";
patch(PartnerListScreen.prototype, {
	
    onClickSundryPartner() {    
        console.log("hello Brother!")
        // var data = this.pos.get_order()
        var all_record = this.pos.partners
        for (let data of all_record){
            if (data.id == 63){
            console.log(data)
            this.state.selectedPartner = data;
            this.props.resolve({ confirmed: true, payload: this.state.selectedPartner });
            this.pos.closeTempScreen();
            this.pos.get_order().setCustomSundry()
            break
            }
        }

        // let orders = this.pos.get_order()
        // this.state.selectedPartner = orders.cashier;
        // this.props.resolve({ confirmed: true, payload: this.state.selectedPartner });
        // this.pos.closeTempScreen();
    }
});