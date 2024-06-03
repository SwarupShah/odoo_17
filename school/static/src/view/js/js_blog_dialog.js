/** @odoo-module **/
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
// import { jsClassDialog } from "./js_blog_dialog";

class jsClassModelInfo extends FormController {
    actionInfoForm() {
        this.env.services.dialog.add(jsClassDialog, {
            resModel: this.props.resModel,
            resDesc: "This is a demo pop-up; feel free to customize the functionality to meet your requirements."
        });
    }
}

jsClassModelInfo.template = "school.modelInfoBtn";

export const modelInfoView = {
    ...formView,
    Controller: jsClassModelInfo,
};

registry.category("views").add("model_info", modelInfoView);
