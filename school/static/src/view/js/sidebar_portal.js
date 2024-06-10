/* @odoo-module */  

import PortalSidebar from "@portal/js/portal_sidebar";

PortalSidebar.include({
    events: {
        "click .o_print_btn": "_onChangeButton",
        // "click .o_portal_invoice_print d-block": "_onChangeButton",
    },
    start: function () {
        this.autoStreetTwo = document.querySelector(".o_portal_sidebar");
        // this.autoFromFirst = document.querySelector(".o_portal_sidebar_content");
        return this._super.apply(this, arguments);
    },
    _onChangeButton: function () {
        console.log("frnjfbruf")
        // console.log(this.autoStreetTwo.querySelectorAll(".o_portal_invoice_print"))
        var button = this.autoStreetTwo.querySelector(".o_portal_sale_sidebar");

        if (button) {          
            // button.textContent = "Janvi";
            button.style.backgroundColor = "#DEDEDE"; 
            // button.style.color = "yellow";
            // var head = this.autoStreetTwo.querySelector("#introduction");
            // head.style.backgroundColor = "green";
            button.style.borderRadius = "30px";
            button.style.padding = "20px";
        }

        // var button1 = this.autoFromFirst.querySelector(".o_portal_sidebar_content");
        // console.log(button1)
        // if (button1) {          
        //     button1.style.backgroundColor = "green"; 
        // }
    },
});