from odoo import http
from odoo.http import request


class NationalIDProgress(http.Controller):

    @http.route('/national_id_application_progress', type='json', auth='user')
    def get_progress(self):
        # Calculate progress based on your criteria
        progress = 33  # Example: 33% progress
        return {'progress': progress}
