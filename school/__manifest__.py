{
    'name' : 'Education Management',
    'version' : '1.1',
    'authors' : 'swarup shah',
    'summary' : 'Education management Management System',
    'description' : 'This is school management system software supported in "odoo 17".',
    'sequence': -1,
    'category' : 'Education',
    'depends' : ['mail','base','sale','sale_management','stock','planning','web','hr_expense','portal','website'],
    'license': 'OPL-1',
    'assets': {
         'web.assets_backend': [
            'school/static/src/view/xml/*.xml',
            'school/static/src/view/js/class_a.js',
            'school/static/src/view/js/class_b.js',
            'school/static/src/view/js/js_blog_dialog.js',
            'school/static/src/view/js/js_button_sale.js',
            'school/static/src/view/js/js_button_he.js',
            'school/static/src/view/js/planning_button.js',
            'school/static/src/view/js/form_user_logo.js'
        ],
        'web.assets_frontend': [
            'school/static/src/view/js/hello.js',
            'school/static/src/view/js/sidebar_portal.js',
            
        ],
    },
    'data':[
        'security/security.xml',
        "security/ir.model.access.csv",
        'security/ir_rules.xml',
        
        'report/ir_actions_report.xml',
        'report/sales_report_template_wizard.xml',
        'report/report_student.xml',
        'report/sale_report.xml',
        'report/filter_data_report.xml',
        'report/res_partner.xml',
        'report/hr_expense_report.xml',

        "data/cron_demo.xml",
        "data/education_management_sequence.xml",
        "data/school_email_tamplate.xml",
        "data/student_mail_template.xml",
        "data/res_partner_template.xml",
        "data/monthly_report.xml",
        "data/order_confirm_email.xml",
        
        "wizard/total_amount_wizard.xml",
        "wizard/anotified_wizard.xml",
        "wizard/cancel_student_wizard_view.xml",
        'wizard/sale_report_wizard.xml',
        'wizard/sale_delivery_wizard.xml',
        'wizard/commission_sale_wizard.xml',
        
        "views/menu.xml",
        "views/school_view.xml",
        'views/student_marks.xml',
        'views/student_result.xml',
        'views/student.xml',
        'views/sale.xml',
        'views/female_student.xml',
        "views/teach.xml",
        "views/subject.xml",
        "views/class_view.xml",
        "views/commission_view.xml",
        "views/commission_view_select.xml",
        "views/commission_order_line.xml",
        "views/courses.xml",
    ],
    
    'installable': True,
    'application': True,
}