{
    # INFORMACIÓN BÁSICA DEL MÓDULO
    # Nombre del módulo que aparecerá en Odoo
    'name': 'Motorent - Renting de Vehículos',

    # Versión del módulo (importante para actualizaciones)
    'version': '1.0',

    # Descripción corta (se muestra en la lista de apps)
    'summary': 'Gestión de clientes, vehículos y contratos de renting',

    # Descripción larga del módulo
    # Se usa para explicar en detalle qué hace el sistema
    'description': '''
        Módulo para gestionar:
        - Clientes
        - Vehículos disponibles
        - Contratos de renting

        Permite además la integración con el módulo de ventas,
        generando pedidos automáticamente desde los contratos.
    ''',

    # Autor del módulo
    'author': 'Tu Nombre',

    # Categoría dentro de Odoo (para clasificar la app)
    'category': 'Servicios',

    # DEPENDENCIAS
    # Módulos necesarios para que este funcione correctamente
    'depends': [
        'base',   # Módulo base de Odoo (obligatorio)
        'sale'    # Necesario para crear pedidos de venta (sale.order)
    ],

    # ARCHIVOS DE DATOS
    'data': [
        # Permisos de acceso (lectura, escritura, etc.)
        'security/ir.model.access.csv',

        # Vistas XML (formularios, listas, menús, botones)
        'views/motorent_views.xml',
    ],

    # RECURSOS FRONTEND (OPCIONAL)
    'assets': {
        'web.assets_backend': [
            # Archivo CSS personalizado para el backend
            'motorent/static/src/css/custom.css',
        ],
    },

    # CONFIGURACIÓN DEL MÓDULO
    # Indica si el módulo se puede instalar
    'installable': True,

    # Si es una aplicación principal (aparece como app)
    'application': True,
}