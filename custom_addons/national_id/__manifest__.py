{
    'name': 'National ID Application',
    'version': '1.0',
    'depends': ['base', 'website', 'website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/national_id_application_views.xml',
        'views/national_id_application_action.xml',
        'views/national_id_menu.xml',
        'views/national_id_tree_view.xml'
    ],
    'installable': True,
    'application': True,

}
