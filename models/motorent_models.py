from odoo import models, fields
from odoo.exceptions import UserError

# MODELO: CLIENTES
class Cliente(models.Model):
    _name = 'motorent.cliente'
    _description = 'Cliente Motorent'

    # Nombre del cliente (obligatorio)
    name = fields.Char(string='Nombre', required=True)

    # Datos de contacto
    telefono = fields.Char(string='Teléfono')
    email = fields.Char(string='Email')

    # Documento identificativo (obligatorio)
    dni = fields.Char(string='DNI/NIE', required=True)

    # Dirección del cliente
    direccion = fields.Char(string='Dirección')

    # Imagen del carnet de conducir (binario)
    foto_carnet = fields.Binary(string='Foto del carnet de conducir')

    # Tipo de situación laboral del cliente
    tipo_contrato_laboral = fields.Selection([
        ('temporal', 'Temporal'),
        ('indefinido', 'Indefinido'),
        ('autonomo', 'Autónomo'),
        ('otro', 'Otro')
    ], string='Tipo de contrato laboral')

    # Relación con el modelo estándar de contactos de Odoo
    # Permite integrar el cliente con otros módulos (ventas, facturación, etc.)
    partner_id = fields.Many2one(
        'res.partner',
        string='Contacto en Odoo',
        required=True
    )

# MODELO: VEHÍCULOS
class Vehiculo(models.Model):
    _name = 'motorent.vehiculo'
    _description = 'Vehículo para renting'

    # Nombre o modelo del vehículo
    name = fields.Char(string='Modelo', required=True)

    # Matrícula del vehículo (obligatoria)
    matricula = fields.Char(string='Matrícula', required=True)

    # Marca del vehículo
    marca = fields.Char(string='Marca')

    # Año de fabricación
    anyo = fields.Char(string='Año')

    # Indica si el vehículo está disponible para alquilar
    disponible = fields.Boolean(string='Disponible', default=True)

    # Número de bastidor (identificador único del vehículo)
    numero_bastidor = fields.Char(string='Número de bastidor')

    # Observaciones adicionales
    observaciones = fields.Text(string='Observaciones')

    # Imagen del vehículo
    imagen = fields.Binary(string='Foto del vehículo')


# MODELO: CONTRATOS
class Contrato(models.Model):
    _name = 'motorent.contrato'
    _description = 'Contrato de renting'

    # Descripción del contrato
    name = fields.Char(string='Descripción', required=True)

    # Relación con el cliente (modelo propio)
    cliente_id = fields.Many2one(
        'motorent.cliente',
        string='Cliente',
        required=True
    )

    # Vehículo asociado al contrato
    vehiculo_id = fields.Many2one(
        'motorent.vehiculo',
        string='Vehículo',
        required=True
    )

    # Fechas del contrato
    fecha_inicio = fields.Date(string='Fecha de inicio')
    fecha_fin = fields.Date(string='Fecha de fin')

    # Coste mensual del renting
    coste_mensual = fields.Float(string='Coste mensual')

    # Datos bancarios
    iban = fields.Char(string='IBAN')
    titular_cuenta = fields.Char(string='Titular de la cuenta')

    # Condiciones del contrato
    seguro_incluido = fields.Boolean(string='Seguro incluido')
    kilometraje_maximo = fields.Integer(string='Kilometraje máximo')

    # Relación con el pedido de venta generado en Odoo
    pedido_venta_id = fields.Many2one(
        'sale.order',
        string='Pedido de Venta'
    )

    # MÉTODO: CREAR PEDIDO DE VENTA AUTOMÁTICO
    def crear_pedido_venta(self):
        """
        Este método crea automáticamente un pedido de venta (sale.order)
        a partir de los datos del contrato.

        Flujo:
        1. Busca el producto "Renting Vehículo"
        2. Crea un pedido de venta asociado al cliente
        3. Añade una línea con el vehículo y el precio mensual
        4. Guarda la relación entre contrato y pedido
        """

        for contrato in self:

            # 1. Buscar el producto de renting
            producto = self.env['product.product'].search([
                ('name', '=', 'Renting Vehículo')
            ], limit=1)

            # Si no existe el producto, se lanza un error
            if not producto:
                raise UserError(
                    "No existe el producto 'Renting Vehículo'. Créalo en Ventas."
                )

            # 2. Crear pedido de venta
            order = self.env['sale.order'].create({
                # Se usa el partner del cliente (modelo estándar de Odoo)
                'partner_id': contrato.cliente_id.partner_id.id,
            })


            # 3. Crear línea del pedido
            self.env['sale.order.line'].create({
                'order_id': order.id,
                'product_id': producto.id,

                # Nombre del producto en la línea (modelo del vehículo)
                'name': contrato.vehiculo_id.name,

                # Cantidad (1 contrato = 1 servicio)
                'product_uom_qty': 1,

                # Precio mensual del contrato
                'price_unit': contrato.coste_mensual,
            })


            # 4. Guardar relación contrato -> pedido

            contrato.pedido_venta_id = order.id