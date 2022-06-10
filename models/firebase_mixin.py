import json
from odoo import _, api, models, fields
from odoo.tools import date_utils

class FirebaseMixin(models.AbstractModel):
    _name = 'firebase.mixin'
    _description = "mixin to send"
    
    def _to_firebase_data(self):
        return json.dumps(self.read()[0], default=date_utils.json_default)
    
    def _firebase_send(self,partner_id, ev=None):
        ev = ev or self._to_firebase_data()
        firebase_bridge_id = self.env['ir.config_parameter'].sudo().get_param('towing.firebase_bridge')
        firebase_bridge = self.env['firebase.bridge'].sudo().browse(int(firebase_bridge_id))
        print("NOTIFY FIREBASE bridge", firebase_bridge)
        if firebase_bridge:
            firebase_bridge.send_to_partner(partner_id,self._name,ev)