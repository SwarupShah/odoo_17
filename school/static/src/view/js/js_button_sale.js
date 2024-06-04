/** @odoo-module **/
import { registry } from '@web/core/registry';
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";

class jsClassModelListInfo extends ListController {
    actionSaleList() {
                alert("Hii Janvii");
    }
}
jsClassModelListInfo.template = "school.modelSaleBtn";

export const modelInfoListView = {
    ...listView,
    Controller: jsClassModelListInfo,
};
registry.category("views").add("model_sale", modelInfoListView);