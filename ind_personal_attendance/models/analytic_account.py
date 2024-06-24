from odoo import fields, models, api

class AnalyticAccount(models.Model):
    _name = 'analytic.account'
    _inherit = 'mail.thread'
    
    code = fields.Char(string="Código", tracking=True, store=True)
    name = fields.Char(string="Centro de Costo", tracking=True, store=True)
    company = fields.Selection(
        [("ind","INDOMIN"),
        ("mec","MECAPARTS S.A.C."),
        ],
        string="Compañía",
        default="ind",
        required=True,
        tracking=True,
    )
    active = fields.Boolean(string='Activo', default=True)
    
    # Obtener el nombre completo del CC
    def name_get(self):
        res = []
        for analytic in self:
            name = analytic.name
            if analytic.code:
                name = '[' + analytic.code + '] ' + name
            res.append((analytic.id, name))
        return res
    
    # Búsqueda de un CC por código o nombre
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|',
                    ('code', operator, name),
                    ('name', operator, name)
                    ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)