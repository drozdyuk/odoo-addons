# -*- coding: utf-8 -*-

{
    'name': 'CRM Auto Mailing',
    'category': 'Hidden',
    'summary': 'CRM Auto Mailing',
    'version': '1.0',
    'description': """CRM Auto Mailing""",
    'author': 'O.drozdyuk',
    'depends': ['crm'],
    'data': [
        'views/crm_auto_mailing_view.xml',
        'views/crm_lead_view.xml',
        'data/data_record.xml',
    ],
    'installable': True,
}
