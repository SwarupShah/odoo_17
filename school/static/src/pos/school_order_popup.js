/** @odoo-module **/
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { onMounted, useRef, useState } from "@odoo/owl";

export class schoolOrderPopup extends AbstractAwaitablePopup {
    static template = "school.schoolOrderPopup";
    static defaultProps = {
        closeText: _t("Cancel"),
        confirmText: _t("Save"),
        title: _t("Create School Order"),
        locations: [],
        amount: 0,
    };
    setup(){
        super.setup();
        this.state = useState({
            inputValue: this.props.startingValue,
            note: '',
            deliveryDate: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
        });
    }
    getPayload(){
        return {
            school: this.state.inputValue,
            note: this.state.note,
            amount: this.props.amount,
            orderDate: this.props.currentDate,
            deliveryDate: this.state.deliveryDate
        };
    }
}
