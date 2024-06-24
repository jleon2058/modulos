from odoo import fields, models

class Employee(models.Model):
    _name = 'employee'
    _description = 'Lista de empleados'
    
    name = fields.Char(string="Nombre")
    dni = fields.Char(string="DNI", size=8)
    email = fields.Char(string="Correo")
    job = fields.Char(string="Puesto")
    photo = fields.Binary(string="Foto del empleado")