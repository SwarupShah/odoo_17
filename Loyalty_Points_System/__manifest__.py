{
    'name': 'Custom Loyalty Points System for Sale Orders',
    'version': '1.0',
    'summary': 'Task Given By Mitesh Sir',
    'author': 'Naman Jain',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/loyalty_points_view.xml',
        'views/SaleOrderInherit_view.xml',
        'reports/customer_loyalty_points_report.xml',
        'wizards/loyalty_wizard.xml',
        'reports/loyalty_points_history_report.xml'
    ],


    'installable': True,
    'application': True,
    'sequence': -20,
}
