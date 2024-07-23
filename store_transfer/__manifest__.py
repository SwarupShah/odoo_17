{
    'name': 'Store Transfer',
    'version': '17.0.0.1',
    'authors': 'swarup shah',
    'summary': 'Implement Custom Object for Store Transfer',
    'description': 'Implement Custom Object for Store Transfer',
    'sequence': -1,
    # 'category': 'sale',
    'depends': ['base','sale','stock'],
    'license': 'OPL-1',
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/store_transfer_view.xml',
    ]
}