# -*- coding: utf-8 -*-
{
    'name': u'Department Contracts Handover',
    'summary': "Department Contracts Handover",
    'author':'CodeIT',
    'version': '1.0.0',
    'category': 'Human Resources/Contracts',
    'help':"""The Contract Administrator can easily share the access to the Employees’ Contracts of the Company Department(s) to any user.

Module allows:

- to choose the Department, which Employees’ Contracts you want to share. 
- to choose a user, the Employees’ Contracts should be shared with.
- to choose if the access to a contract of the Department Manager should be shared.
- to choose an Expiration date till when the Contracts' access is shared.
- to see a list of all the sharing records with the possibility to delete the record and thus revoke the access sharing.""",
    'depends': ['hr_contract'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/rule_views.xml',
        'views/hr_contracts_views.xml',
        'data/ir_crone.xml'
        ],
    'installable': True,
}
