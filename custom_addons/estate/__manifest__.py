{
    'name':'Real estate',
    'version':'1.0',
    'author':'Bob Alexander',
    'website':'www.realestateadvs.edu',
    'depends':[],

    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'data/estate_menus.xml',
        'views/list_view.xml',
        'views/form_view.xml',
        'views/search_view.xml',
        'data/estate_property_type_action.xml',
        'data/estate_property_type_menu.xml',
        'views/estate_property_type_list_view.xml',
        'views/estate_property_type_form_view.xml',
        'data/estate_property_tag_menu.xml',
        'data/estate_property_tag_action.xml',
        'views/estate_property_tag_tree.xml',

        'views/estate_property_tag_form.xml',
        'views/estate_property_offer_formview.xml',
        'views/estate_property_offer_treeview.xml',
        'views/res_user_view_form.xml'

    ],
    'installable':True,
    'application':True,
}