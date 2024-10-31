{
    'name': 'Bank Statement Normalization',
    'version': '1.0',
    'summary': 'Normalize bank statements for multiple banks',
    'description': '''
    This module processes bank statements from different banks and normalizes them into a common format.
    ''',
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/bank_statement_normalization_view.xml',
    ],
    'installable': True,
    'application': True,
}