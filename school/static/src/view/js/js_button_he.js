/** @odoo-module **/
import { ListController } from "@web/views/list/list_controller";
import { listView } from "@web/views/list/list_view";
import { registry } from '@web/core/registry';

class jsClassModelhr extends ListController {
    setup() {
        super.setup();
        this.orm = useService('orm');
        this.actionService = useService('action');
        this.rpc = useService("rpc");
        this.user = useService("user");
        this.isExpenseSheet = this.model.config.resModel === "hr.expense.sheet";

        onWillStart(async () => {
            this.userIsExpenseTeamApprover = await this.user.hasGroup("hr_expense.group_hr_expense_team_approver");
            this.userIsAccountInvoicing = await this.user.hasGroup("account.group_account_invoice");
        });
    }
    async actionhrList() {
        const records = this.model.root.selection;
        const res = await this.orm.call(this.model.config.resModel, 'get_expenses_to_submit', [records.map((record) => record.resId)]);
        if (res) {
            await this.actionService.doAction(res, {});
        }
    }
}

jsClassModelhr.template = "school.modelHrBtn";

export const modelListView = {
    ...listView,
    buttonTemplate: 'hr_expense.ListButtons',
    Controller: jsClassModelhr,
};

registry.category("views").add("model_hr", modelListView);
