# -*- coding: utf-8 -*-

{
    'name': 'Project Access Control',
    'category': 'Hidden',
    'summary': 'Project Access Control',
    'version': '1.0',
    'description': """Project Access Control""",
    'author': 'O.Drozdyuk',
    'depends': ['project_issue'],
    'data': [
        'views/project_access_control_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
