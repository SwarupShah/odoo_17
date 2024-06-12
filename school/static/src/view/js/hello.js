/** @odoo-module **/

import {WebsiteSale} from "@website_sale/js/website_sale";

WebsiteSale.include({
    events: {
        "change select[name='state_id']": "_onChangeState",
        "change select[name='city_id']": "_onChangeCity",
        "input input[name='street2']": "_inputAdd",
        "keyup .form-control ": "_onInputKeyup",
        "keydown .form-control ": "_onInputKeydown",
        
    },
    start: function () {
        this.autoStateCity = document.querySelector(".div_street2");
        this.autoStreetTwo = document.querySelector(".o_wsale_address_fill");
        return this._super.apply(this, arguments);
    },
    _onChangeState: function () {
        console.log("This is Click event")
        this.autoStateCity.querySelectorAll("input").forEach((input) => {
                                input.value = "fgrwfgitruiftug";
                            });
    },
    _inputAdd: function(){
        var button = this.autoStreetTwo.querySelectorAll(".form-control ");
        // button.style.color = "#FCFCFC";
        console.log("This is input event")
    },
    _onInputKeyup: function (event) {
        console.log("Keyup pressed: " + event.key);
    },
    _onInputKeydown: function (event) {
        console.log("Keydown pressed: " + event.key);
    },
});
