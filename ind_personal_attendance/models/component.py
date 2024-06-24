from odoo import fields, models

class Component(models.Model):
    _name = 'component'
    _description = 'Componentes'
    _inherit = 'mail.thread'
    
    name = fields.Char(string = "Nombre", tracking=True, store=True)
    code = fields.Char(string = "Código")