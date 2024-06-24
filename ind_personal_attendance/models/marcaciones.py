from odoo import fields, models, api, _
from datetime import datetime, time, timedelta
import pytz
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

_STATES = [
    ("to_do", "Por iniciar"),
    ("doing", "En progreso"),
    ("done", "Finalizado"),
]

class Marcaciones(models.Model):
    _name = 'marcaciones'
    _inherit = 'mail.thread'
    
    @api.depends("state")
    def _compute_is_editable(self):
        for rec in self:
            if rec.state in ("to_do", "doing", "done"):
                rec.is_editable = False
            else:
                rec.is_editable = True
    
    @api.depends("start_time","end_time")
    def _compute_work_time(self):
        """ for record in self:
            if record.start_time and record.end_time:
                # Calcular la diferencia en horas
                timedelta = record.end_time - record.start_time
                hours_worked = int(timedelta.total_seconds() % 3600)

                # Asignar el resultado al campo work_time
                record.work_time = hours_worked
            else:
                record.work_time = 0.0 """
        for record in self:
            if record.start_time and record.end_time:
                # Calcular la diferencia en horas
                time_difference = record.end_time - record.start_time
                hours, remainder = divmod(time_difference.seconds, 3600)
                minutes = remainder // 60
                # Asignar el resultado al campo work_time
                record.work_time = "{:02d} horas y {:02d} minutos".format(hours, minutes)
            else:
                record.work_time = ""
    
    @api.model
    def _get_default_employee(self):
        return self.env["res.users"].browse(self.env.uid)
    
    @api.constrains('state')
    def _check_previous_tasks_done(self):
        # Verifica que todas las tareas anteriores estén en "done" antes de crear una nueva tarea
        for rec in self:
            previous_tasks = self.search([
                ('employee', '=', rec.employee.id),
                ('id', '<', rec.id),  # Tareas anteriores
            ])
            if previous_tasks and any(task.state != 'done' for task in previous_tasks):
                raise ValidationError("No puedes crear una nueva tarea si hay tareas anteriores pendientes")
    
    """ @api.model
    def export_data(self, fields_to_export):
        
        campos_restringidos = ['responsible', 'analytic_account', 'state']
        
        # Verificar si el usuario pertenece al grupo que tiene permiso para exportar el campo restringido
        for campo in campos_restringidos:    
            if campo in fields_to_export and not self.env.user.has_group('ind_personal_attendance.group_attendance_manager'):
                fields_to_export.remove(campo)

        return super(Marcaciones, self).export_data(fields_to_export) """
    
    
    employee = fields.Many2one(
        comodel_name='res.users',
        string="Empleado",
        required=True,
        copy=False,
        tracking=True,
        default=_get_default_employee,
        index=True
    )
    responsible = fields.Many2one(
        comodel_name='res.users',
        string="Supervisor",
        required=False,
        copy=True,
        tracking=True,
        index=True,
        domain=[('responsable', '=', True)]
    )
    name = fields.Many2one(
        comodel_name='task',
        string="Actividad",
        copy=False,
        tracking=True,
        index=True,
        ondelete='restrict'
    )
    analytic_account = fields.Many2one(
        comodel_name='analytic.account',
        string="Centro de Costo",
        required=True,
        tracking=True,
        ondelete="restrict"
        )
    component = fields.Many2one(
        comodel_name="component",
        string="Componente",
        tracking=True,
        ondelete="restrict"
    )
    description = fields.Char(string="Descripción")
    start_time = fields.Datetime(string="Hora de Inicio", copy=False)
    end_time = fields.Datetime(string="Hora de Fin", copy=False)
    employee_photo = fields.Binary(string="Foto del empleado", store=True)
    state = fields.Selection(
        selection = _STATES,
        string = "Estado",
        index = True,
        tracking = True,
        required = True,
        copy = False,
        default = "to_do",
    )
    is_editable = fields.Boolean(compute="_compute_is_editable", readonly=True)
    work_time = fields.Char(string="Horas Trabajadas", compute="_compute_work_time")
    
    def button_finish_lunch(self):
        almuerzo = datetime.combine(datetime.today().date(), time(8,50))
        _logger.info(almuerzo)
        fecha_actual = datetime.now()
        _logger.info(fecha_actual)
        hora_corte = time(8, 50, 0)
        _logger.info(hora_corte)
        fecha_corte = datetime.combine(fecha_actual.date(), hora_corte)
        _logger.info(fecha_corte)
        
        activities_to_finalize = self.search([('state', '=', 'doing'), ('start_time', '<', fecha_corte)])
        _logger.info(activities_to_finalize)
        _logger.info("Finalización de actividades")
        for activity in activities_to_finalize:
            activity.button_done()
            activity.end_time = almuerzo
            _logger.info("-----Ingreso al for de BTL")
            if fecha_actual.weekday() != 5:
                activity.crear_nuevo_registro(activity)
            
    @api.model
    def crear_nuevo_registro(self, registro_anterior_id):
        _logger.info("Inicio de CNR")
        # Obtener el registro anterior
        registro_anterior = self.browse(registro_anterior_id.id)

        hora_inicio= time(18, 0, 0)
        start_time = datetime.combine(datetime.today(), hora_inicio)
        _logger.info(hora_inicio)
        _logger.info(start_time)
        
        # Crear un nuevo registro con los datos del registro anterior
        nuevo_registro_vals = {
            'employee': registro_anterior.employee.id,
            'responsible': registro_anterior.responsible.id,
            'analytic_account': registro_anterior.analytic_account.id,
            'name': registro_anterior.name.id,
            'component': registro_anterior.component.id,
            'description': registro_anterior.description,
            'start_time': start_time,
            'state': 'doing',
            # Agrega otros campos según tus necesidades
        }
        
        _logger.info(nuevo_registro_vals)
        _logger.info("Final de los valores en nuevos registros")
        
        _logger.info("Inicio de valor en nuevo registro")
        nuevo_registro = self.create(nuevo_registro_vals)
        _logger.info(nuevo_registro)
        _logger.info("Final de valor en nuevo registro")
        
        """ view_id = self.env.ref('ind_personal_attendance.marcaciones_form').id
        _logger.info("Inicio de la vista") """
        """ return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model':'ind_personal_attendance.marcaciones',
            'view_id': view_id,
            'res_id': nuevo_registro.id,
            'target': 'main',
        } """
    
    def button_finish_all(self):
        hora = 18
        minutos = 0
        """ zona_horaria_gmt = pytz.timezone('GMT') """
        """ lima_timezone = pytz.timezone('America/Lima') """
        activities_to_finalize = self.search([('state', '=', 'doing')])
        for activity in activities_to_finalize:
            activity.button_done()
            """ date_time_now = datetime.now(tz=zona_horaria_gmt)
            activity.end_time = datetime.combine(date_time_now.date() , time(hora, minutos, 0)) """
            if hora < 19:
                activity.end_time = datetime.combine(datetime.today() - timedelta(days=1), time(hora+5, minutos, 0))
            else:
                activity.end_time = datetime.combine(datetime.today() , time(hora+5-24, minutos, 0))
    
    def button_start(self):
        self.state = "doing"
        self.start_time = fields.Datetime.now()
    
    def button_done(self):
        self.state = "done"
        self.end_time = fields.Datetime.now()
    
    def button_restart(self):
        self.state = "doing"
        self.end_time = False
        