from odoo import models

class EmployeeExcelReport(models.AbstractModel):
    _name = 'report.university_employee.excel_export'
    
    def generate_xlsx_report(self, data, response):
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/export/xlsx?model=hr.employee&domain=[("disability","=",True)]',
            'target': 'new',
        }