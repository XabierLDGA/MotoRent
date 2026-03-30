from odoo import models, fields
from odoo.exceptions import UserError

# ================= Clientes =================
class Cliente(models.Model):
    _name = 'motorent.cliente'
    _description = 'Cliente Motorent'

    name = fields.Char(string='Nombre', required=True)
    telefono = fields.Char(string='Teléfono')
    email = fields.Char(string='Email')

    dni = fields.Char(string='DNI/NIE', required=True)
    direccion = fields.Char(string='Dirección')
    foto_carnet = fields.Binary(string='Foto del carnet de conducir')

    tipo_contrato_laboral = fields.Selection([
        ('temporal', 'Temporal'),
        ('indefinido', 'Indefinido'),
        ('autonomo', 'Autónomo'),
        ('otro', 'Otro')
    ], string='Tipo de contrato laboral')

    # Conexión con contactos oficiales
    partner_id = fields.Many2one(
        'res.partner',
        string='Contacto en Odoo',
        required=True
    )


# ================= Vehículos =================
class Vehiculo(models.Model):
    _name = 'motorent.vehiculo'
    _description = 'Vehículo para renting'

    name = fields.Char(string='Modelo', required=True)
    matricula = fields.Char(string='Matrícula', required=True)
    marca = fields.Char(string='Marca')
    anyo = fields.Char(string='Año')
    disponible = fields.Boolean(string='Disponible', default=True)

    numero_bastidor = fields.Char(string='Número de bastidor')
    observaciones = fields.Text(string='Observaciones')
    imagen = fields.Binary(string='Foto del vehículo')


# ================= Contratos =================
class Contrato(models.Model):
    _name = 'motorent.contrato'
    _description = 'Contrato de renting'

    name = fields.Char(string='Descripción', required=True)

    # Usamos nuestro cliente
    cliente_id = fields.Many2one(
        'motorent.cliente',
        string='Cliente',
        required=True
    )

    vehiculo_id = fields.Many2one(
        'motorent.vehiculo',
        string='Vehículo',
        required=True
    )

    fecha_inicio = fields.Date(string='Fecha de inicio')
    fecha_fin = fields.Date(string='Fecha de fin')
    coste_mensual = fields.Float(string='Coste mensual')

    iban = fields.Char(string='IBAN')
    titular_cuenta = fields.Char(string='Titular de la cuenta')
    seguro_incluido = fields.Boolean(string='Seguro incluido')
    kilometraje_maximo = fields.Integer(string='Kilometraje máximo')

    #  Enlace con Ventas
    pedido_venta_id = fields.Many2one(
        'sale.order',
        string='Pedido de Venta'
    )

    #  Botón para crear pedido automáticamente
    def crear_pedido_venta(self):
        for contrato in self:

            # Buscar producto de renting
            producto = self.env['product.product'].search([
                ('name', '=', 'Renting Vehículo')
            ], limit=1)

            if not producto:
                raise UserError("No existe el producto 'Renting Vehículo'. Créalo en Ventas.")

            # Crear pedido
            order = self.env['sale.order'].create({
                'partner_id': contrato.cliente_id.partner_id.id,
            })

            # Crear línea del pedido
            self.env['sale.order.line'].create({
                'order_id': order.id,
                'product_id': producto.id,
                'name': contrato.vehiculo_id.name,
                'product_uom_qty': 1,
                'price_unit': contrato.coste_mensual,
            })

            # Guardar relación
            contrato.pedido_venta_id = order.id
