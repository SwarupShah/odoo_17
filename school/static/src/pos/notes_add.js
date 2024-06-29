/** @odoo-module **/

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    // init_from_JSON(json) {
    //     super.init_from_JSON(...arguments);
    //     this.customer_note = "hello brother";
    // },
    
    // export_as_JSON() {
    //     const result = super.export_as_JSON(...arguments);
    //     result.note = this.getCustomNote();
    //     return result;
    // },

    export_as_JSON() {
        const result = super.export_as_JSON(...arguments);
        result.note = this.note || "";
        return result;
    },
    setCustomNote(note) {
        this.note = note;
    },
});
// patch(Order.prototype, {
//     // init_from_JSON(json) {
//     //     super.init_from_JSON(...arguments);
//     //     this.customer_note = "hello brother";
//     // },
    
//     export_as_JSON() {
//         const json = super.export_as_JSON(...arguments);
//         json['customer_note'] = this.getCustomNote()
//         return json
//     },

//     export_as_JSON() {
//         const result = super.export_as_JSON(...arguments);
//         result.note = this.getCustomNote();
//         return result;
//     },
//     getCustomNote() {
//         return this.note || "";
//     },
//     setCustomNote(note) {
//         this.note = note;
//     },
// });
// import { Order } from "@point_of_sale/app/store/models";
// import { patch } from "@web/core/utils/patch";

// patch(Order.prototype, {
//     init: function () {
//         super.init(this, arguments);
//         this.customer_note = "";
//     },

//     set_customer_note: function (note) {
//         this.customer_note = note;
//     },

//     export_as_JSON: function () {
//         const json = super.export_as_JSON(...arguments);
//         json['customer_note'] = "hello brother"
//         return json
//     }
// });

/* @odoo-module */

// import { _t } from "@web/core/l10n/translation";
// import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
// import { useService } from "@web/core/utils/hooks";
// import { TextAreaPopup } from "@point_of_sale/app/utils/input_popups/textarea_popup";
// import { Component } from "@odoo/owl";
// import { usePos } from "@point_of_sale/app/store/pos_hook";
// import { Order } from "@point_of_sale/app/store/models";
// import { patch } from "@web/core/utils/patch";

// export class CustomerNoteButton extends Component {
//     static template = "point_of_sale.addNotes";

//     setup() {
//         this.pos = usePos();

//         this.popup = useService("popup");
//     }
//     async onClick() {
//        const order = this.pos.get_order();
//          const orderLines = this.pos.get_order().get_orderlines();
//         if (!orderLines) {
//             return;
//         }
//         const { confirmed, payload: inputNote } = await this.popup.add(TextAreaPopup, {
// //            startingValue: Orderline.get_customer_note(),
//             title: _t("Add Customer Note"),
//         });

//         if (confirmed) {
// //         for (let orderLine of orderLines){
// //            orderLine.set_customer_note(inputNote);
//             let note = document.getElementsByClassName('customNote');
//             if(note.length > 0){
//             var value = note[0]
//             value.innerText=inputNote;
// }
// //          }
// order.setCustomNote(inputNote);
//         }
//     }
// }

// ProductScreen.addControlButton({
//     component: CustomerNoteButton,
// });

// patch(Order.prototype, {
//     export_as_JSON() {
//         const result = super.export_as_JSON(...arguments);
//         result.note = this.getCustomNote();
//         return result;
//     },
//     getCustomNote() {
//         return this.note || "";
//     },
//     setCustomNote(note) {
//         this.note = note;
//     },
// });
