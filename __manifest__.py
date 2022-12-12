# -*- coding: utf-8 -*-
{
    'name': "Climbing gym Web Registration Membership",
    # climbing_gym_portal_membership_registration
    'summary': """
        Climbing gym Web Registration Membership""",

    'description': """
        Climbing gym Web Registration Membership
    """,

    'author': "Miguel Hatrick",
    'website': "http://www.dacosys.com",

    'category': 'Climbing Gym',
    'version': '12.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mail',
                'climbing_gym',
                'climbing_gym_website',
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        # 'views/career.xml',
        # 'views/course.xml',

        # 'views/membership_registration.xml',
        # 'views/menu.xml',

        #'views/portal/portal_my_documents.xml',
        # 'views/portal/portal_course.xml'

        #'views/portal/portal_layout_sidebar.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
