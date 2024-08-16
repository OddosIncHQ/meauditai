{
    'name': 'Bank Statement Normalization',
    'version': '1.0',
    'summary': 'Normalize bank statements for multiple banks',
    'description': '''
    This module processes bank statements from different banks and normalizes them into a common format.
    ''',
    'author': 'Oddos Solutions LLC',
    'depends': ['base'],
    'data': [
        'views/bank_statement_normalization_view.xml',
    ],
    'installable': True,
    'application': True,
}
