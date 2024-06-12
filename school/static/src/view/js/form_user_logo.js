/** @odoo-module **/
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useEffect, useRef, useState } from "@odoo/owl";
import { useBus } from "@web/core/utils/hooks";
import {FormStatusIndicator} from "@web/views/form/form_status_indicator/form_status_indicator"

class jsClassModelIcon extends FormStatusIndicator {
    // setup() {
    //     // this.state = useState({
    //     //     fieldIsDirty: false,
    //     // });
    //     // useBus(
    //     //     this.props.model.bus,
    //     //     "FIELD_IS_DIRTY",
    //     //     (ev) => (this.state.fieldIsDirty = ev.detail)
    //     // );
    //     // useEffect(
    //     //     () => {
    //     //         if (!this.props.model.root.isNew && this.indicatorMode === "invalid") {
    //     //             this.saveButton.el.setAttribute("disabled", "1");
    //     //         } else {
    //     //             this.saveButton.el.removeAttribute("disabled");
    //     //         }
    //     //     },
    //     //     () => [this.props.model.root.isValid]
    //     // );
    //     // super.setup();
    //     this.notificationService = useService("notification");
    //     this.account_move_service = useService("account_move");
    //     this.actionService = useService('action');
    // }
    
    async actionFormIcon() {
        // await this.props.actionFormIcon();
        console.log("hello brother");
        // this.notificationService.add("You closed a deal!", {
        //     title: "OOPS!",
        //     type: "warning",
        //     buttons: [
        //         {
        //             name: "See your Commission",
        //             onClick: () => {
        //                 this.actionService.doAction("commission_action");
        //             },
        //         },
        //     ],
        //   });
    }
}

jsClassModelIcon.template = "school.modelSchoolIconForm";
jsClassModelIcon.props = {
    model: Object,
    actionFormIcon: Function,
};
export const modelIconView = {
    ...formView,
    Controller: jsClassModelIcon,
};

registry.category("views").add("school_view_form", modelIconView);
