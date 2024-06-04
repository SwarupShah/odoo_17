/** @odoo-module **/
import { registry } from '@web/core/registry';
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";

class jsClassModelhr extends ListController {
    setup() {
        super.setup();
        console.log("hello")
    }

    actionhrList() {
        // Implement your button click logic here
        // For now, let's just show a notification
        alert("hello")
    }
}


jsClassModelhr.template = "school.modelHrBtn";


export const modelHrListView = {
    ...listView,
    Controller: jsClassModelhr,
};


registry.category("views").add("model_hr", modelHrListView);
