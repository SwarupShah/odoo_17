/* @odoo-module */  
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.s_website_form_my = publicWidget.Widget.extend({
    selector: '.s_website_form_my',
    
    start: function () {
        this._super.apply(this,arguments);
        this._bindEvents();
        this.passwordInput = document.querySelector(".password_input");
        this.errorMessage = document.querySelector("#s_website_form_result_my");
    },

    _bindEvents: function () {
        this.$('.s_website_form_send_my').on('click', this._send.bind(this));
    },

    _send: function () {
        var password = this.passwordInput.value;

        const passwordError = this._validatePassword(password);
        if (passwordError == "success"){
            console.log(passwordError)
            this.$el.find('form').submit();
        }else{
            console.log(passwordError)
            this.errorMessage.textContent = passwordError;
        }
    },
    _validatePassword: function (password) {
        const minLength = 8;
        const capitalLetter = /[A-Z]/;
        const smallLetter = /[a-z]/;
        const number = /[0-9]/;
        const specialCharacter = /[!@#$%^&*(),.?":{}|<>]/;

        if (password.length < minLength) {
            return 'Password must be at least 8 characters long.';
        }
        if (!capitalLetter.test(password)) {
            return 'Password must contain at least one uppercase letter.';
        }
        if (!smallLetter.test(password)) {
            return 'Password must contain at least one lowercase letter.';
        }
        if (!number.test(password)) {
            return 'Password must contain at least one number.';
        }
        if (!specialCharacter.test(password)) {
            return 'Password must contain at least one special character.';
        }
        return 'success';
    },

});

export default publicWidget.registry.s_website_form_my;