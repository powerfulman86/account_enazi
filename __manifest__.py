# -*- coding: utf-8 -*-
{
    'name': "Enazi Account Customization",

    'description': """
        Enazi Account Customization
    """,

    'author': "CubicIt Egypt",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],
    "external_dependencies": {"python": ["dateutil"]},
    # always loaded
    'data': [
        'views/account_move.xml',
        'templates/invoice_document.xml',
        "templates/activity_statement.xml",
        "templates/outstanding_statement.xml",
        "templates/aging_buckets.xml",
        "views/assets.xml",
        "wizard/statement_wizard.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
