/** @odoo-module **/
import { registry } from '@web/core/registry';
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from '@web/core/utils/hooks';
import { A } from "./class_a";

// A.include({
//     /**
//      * @override
//      */
//     async _methodA(){
//         console.log("new_method")
//     }
// });

class jsClassModelListInfo extends ListController {
    setup() {
        super.setup();
        this.orm = useService('orm');
        this.user = useService("user");
        this.isExpenseSheet = this.model.config.resModel === "hr.expense.sheet";
    }
    async actionSaleList() {
        const records = this.model.root.selection;
        console.log(records)
        const res = this.orm.call(this.model.config.resModel, 'print_report',[records.map((record) => record.resId)]);
        // if (res) {
        //     await this.actionService.doAction(res, {});
        // }
    }
}
jsClassModelListInfo.template = "school.modelSaleBtn";

export const modelInfoListView = {
    ...listView,
    Controller: jsClassModelListInfo,
};
registry.category("views").add("model_sale", modelInfoListView);