from odoo import models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_open_label_layout(self):
        action = self.env['ir.actions.act_window']._for_xml_id('garazd_product_label.action_print_label_from_picking')
        action['context'] = {'default_picking_ids': self.ids, 'active_model': 'stock.picking'}
        return action