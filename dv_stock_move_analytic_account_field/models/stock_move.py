from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    picking_type_code = fields.Selection(
        related='picking_type_id.code', store=True)
    
    def _default_account_analytic_id(self):
        account_analytic_id = False
        if 'default_picking_id' in self.env.context:
            picking_id = self.env['stock.picking'].browse(self.env.context['default_picking_id'])
            account_analytic_id = picking_id.account_analytic_id.id
        return account_analytic_id
    
    account_analytic_id = fields.Many2one(
        'account.analytic.account', string='Centro de Costo', default=_default_account_analytic_id)

    def _prepare_common_svl_vals(self):
        res = super(StockMove, self)._prepare_common_svl_vals()
        res['account_analytic_id'] = self.account_analytic_id.id if self.account_analytic_id else False
        return res
