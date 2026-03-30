{
    'name': 'Motorent - Renting de Vehículos',
    'version': '1.0',
    'summary': 'Gestión de clientes, vehículos y contratos de renting',
    'description': 'Módulo para gestionar clientes, vehículos disponibles y contratos de renting en Motorent.',
    'author': 'Tu Nombre',
    'category': 'Servicios',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/motorent_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'motorent/static/src/css/custom.css',
        ],
    },
    'installable': True,
    'application': True,
}
