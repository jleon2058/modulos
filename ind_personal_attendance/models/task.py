from odoo import api, models, fields

class Task(models.Model):
    _name = 'task'
    _inherit = 'mail.thread'
    
    name = fields.Char(string="Actividad", tracking=True, store=True)
    description = fields.Char(string="Descripción", tracking=True, store=True)