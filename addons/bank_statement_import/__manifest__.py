{
    'name': 'Bank Statement Import',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Import bank statements from Excel files',
    'description': """
        This module allows users to import bank statement transactions from .xlsx files.
    """,
    'author': 'Your Name',
    'depends': ['base', 'account'],
    'data': [
        'views/bank_statement_import_wizard_view.xml',
        'views/bank_statement_menu.xml',
    ],
    'installable': True,
    'application': False,
}
