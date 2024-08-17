{
    'name': 'Custom Consolidated Data Module',
    'version': '17.0',
    'summary': 'Module to manage declarative data and CSV processing',
    'description': 'This module handles activity codes, forms, offices, contributor types, sworn declarations, and entity types, with CSV processing capabilities.',
    'category': 'Custom',
    'author': 'Oddos Solutios LLC',
    'depends': ['base', 'documents'],
    'data': [
        'views/consolidated_data_views.xml',
        'views/csv_upload_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
