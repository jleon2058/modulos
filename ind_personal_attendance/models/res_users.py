from odoo import fields, models

class Users(models.Model):
    _inherit = 'res.users'
    
    responsable = fields.Boolean(string="Asigna tareas", default=False)