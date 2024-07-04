/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { schoolOrderPopup } from "@school/pos/school_order_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

export class SchoolButton extends Component {
    static template = "point_of_sale.schoolOrderTemplate";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
        this.orm = useService("orm");
    }

    async onClick() {
        const selectedOrderline = this.pos.get_order().get_selected_orderline();
        const order = this.pos.get_order();
        
        if (!selectedOrderline) {
            return;
        }
        let status = true;
        while(status){
            const data = await this.orm.call('school.profile', 'get_school_data', ['true']);
            console.log(data);

            const { confirmed, payload } = await this.popup.add(schoolOrderPopup, {
                title: _t("Create School Order"),
                data: data,
                amount: this.pos.get_order().get_total_with_tax(),
                currentDate: new Date().toISOString().split('T')[0],
            });

            if (confirmed) {
                if (!payload.school){
                    await this.popup.add(ErrorPopup, {
                        title: _t("Invalid Location"),
                        body: _t("Please select the proper location."),
                        cancelKey: true,
                    });
                }
                else{
                    console.log(payload.school)
                    break
                }
            }
            else{
                break
            }
        }
    }
}

ProductScreen.addControlButton({
    component: SchoolButton,
    condition: function () {
        return this.pos.config.enable_school;
    },
});
