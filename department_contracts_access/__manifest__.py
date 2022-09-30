# -*- coding: utf-8 -*-
{
    'name': 'Department Contracts Access and Handover',
    'summary': "Grants Department Manager access to Contracts of Department's Employees. Enables admin to share access to a specific Department Contracts.",
    'author': 'CodeIT',
    'company': 'CodeIT',
    'website': 'https://codeit.us/',
    'version': '14.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'description':
        """The module enables the Department Manager to have read-only access to the Contracts of their Department’s Employees by creating a new Contracts group - “Contracts Manager”. The User is assigned to the Contracts Manager group in Settings>Manage Users>Specific User>HR Section>Contracts select.
        The module also enables the Contracts Administrator to share the access to the Employees’ Contracts of any Company Department(s) with any User within the 

        Contracts Manager group. It allows:

        - choosing the Department whose Employees’ Contracts you want to share;
        - choosing a User the Employees’ Contracts should be shared with;
        - choosing if the access to the Contract of the Department Manager should be shared;
        - choosing an expiration date till when the access is shared and providing infinite access if no expiration date is specified;
        - seeing a list of all the sharing records with the possibility to delete the record and thus revoke the access sharing.

        After the Employees’ Contracts of any Company Department(s) are shared with the Contracts Manager by the Contracts Administrator, the system provides the Contracts Manager with read-only access to these Contracts even if the User is not the Department Manager of that unit.

        Module installation:

        1. Copy the module folder to the “Odoo app” directory on your server;
        2. Restart the Odoo server;
        3. Go to Settings -> Developer Tools;
        4. Activate the Developer Mode;
        5. Go to Apps and push the “Update Apps List” button;
        6. Find and install the required modules: hr, hr_contract;
        7. Find the “Department Contracts Access and Handover” module and push the “Install” button.
        """,
    'images': ['static/description/banner.png'],
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
