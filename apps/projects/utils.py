#!/usr/bin/env python
# -*- coding: utf-8 -*-
from natr.settings import EXCEL_REPORTS_DIR
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side, Color, colors, PatternFill
from openpyxl.cell import get_column_letter


class ExcelReport:
    assignments = []
    assig_intervals = [
        'Никогда',
        'Еженедельно',
        'Ежемесячно',
        'Ежеквартально',
        'Каждые полгода',
        'Ежегодно'
    ]
    assig_statuses =  [
        'Не назначено',
        'Назначено',
        'Отправлено на доработку',
        'Исполнение продолжается',
        'На утверждении',
        'Утверждено',
        'Исполнено'
    ]
    alignment_left=Alignment(horizontal='left',
                    vertical='top',
                    text_rotation=0,
                    wrap_text=True,
                    shrink_to_fit=False,
                    indent=0)
    alignment_center=Alignment(horizontal='center',
                    vertical='top',
                    text_rotation=0,
                    wrap_text=True,
                    shrink_to_fit=False,
                    indent=0)

    alignment_header=Alignment(horizontal='center',
                    vertical='center',
                    text_rotation=0,
                    wrap_text=True,
                    shrink_to_fit=False,
                    indent=0)
    border = Border(left=Side(border_style='thin', color=Color(rgb='FF000000')),
                 right=Side(border_style='thin', color=Color(rgb='FF000000')),
                 top=Side(border_style='thin', color=Color(rgb='FF000000')),
                 bottom=Side(border_style='thin', color=Color(rgb='FF000000')))
    yellowFill = PatternFill(start_color='FFFFC001',
                   end_color='FFFFC001',
                   fill_type='solid')

    def __init__(self, report=None):
        self.report = report

    def insert_into_cell(self, ws, column, cell_number, string):
        if not string:
            string = ""
        if type(cell_number) == int:
            cell_number = str(cell_number)
        if type(string) == int:
            string = str(string)
        ws[column+cell_number] = string
        if ws.column_dimensions[column].width < len(string):
            ws.column_dimensions[column].width = len(string) + 3
        # ws[column+cell_number].border = self.border
        return ws


    def generate_excel_report(self):
        report = self.report
        project = report.project
        milestone = report.milestone
        wb = Workbook()
        ws1 = wb.active
        ws1.title = u'Общая информация'

        ws1 = self.insert_into_cell(ws1, 'A', '1', u'Дата отчета')
        ws1 = self.insert_into_cell(ws1, 'A', '2', u'Наименование грантополучателя')
        ws1 = self.insert_into_cell(ws1, 'A', '3', u'Номер и дата договора')
        ws1 = self.insert_into_cell(ws1, 'A', '4', u'Цель гранта')
        ws1 = self.insert_into_cell(ws1, 'A', '5', u'Сумма гранта')
        ws1 = self.insert_into_cell(ws1, 'A', '6', u'Период отчетности')
        ws1 = self.insert_into_cell(ws1, 'A', '7', u'Достигнутые результаты грантового проекта')
        ws1 = self.insert_into_cell(ws1, 'A', '8', u'Наименование охранного документа (в случае наличия)')
        ws1 = self.insert_into_cell(ws1, 'A', '9', u'Номер и дата выдачи охранного документа (в случае наличия)')

        ws1 = self.insert_into_cell(ws1, 'B', '1', report.date)
        ws1 = self.insert_into_cell(ws1, 'B', '2', project.organization_details.name if project is not None else "")
        contract_number_date = "{0}, {1}".format(project.aggreement.document.number, project.aggreement.document.date_sign) if project is not None else ""
        ws1 = self.insert_into_cell(ws1, 'B', '3', contract_number_date)
        ws1 = self.insert_into_cell(ws1, 'B', '4', project.grant_goal if project is not None else "")
        ws1 = self.insert_into_cell(ws1, 'B', '5', "{0} {1}".format(milestone.fundings.amount, milestone.fundings.currency) if milestone is not None else "")
        ws1 = self.insert_into_cell(ws1, 'B', '6', report.period if project is not None else "")
        ws1 = self.insert_into_cell(ws1, 'B', '7', report.results if project is not None else "")



        ws2 = wb.create_sheet()
        ws2.title = u'Бюждетные средства'

        ws2 = self.insert_into_cell(ws2, 'A', '1', u'Номер п/п')
        ws2 = self.insert_into_cell(ws2, 'B', '1', u'Статьи затрат по договору')
        ws2 = self.insert_into_cell(ws2, 'C', '1', u'Документы по отчету грантополучателя за Этап № {0}'.format(milestone.number))
        ws2 = self.insert_into_cell(ws2, 'D', '1', "")
        ws2 = self.insert_into_cell(ws2, 'E', '1', "")
        ws2 = self.insert_into_cell(ws2, 'F', '1', "")
        ws2 = self.insert_into_cell(ws2, 'G', '1', "")
        ws2 = self.insert_into_cell(ws2, 'H', '1', "")
        ws2.merge_cells('C1:H1')
        ws2['C1'].alignment = self.alignment_center
        ws2.merge_cells('A1:A2')
        ws2['A1'].alignment = self.alignment_center
        ws2.merge_cells('B1:B2')
        ws2['B1'].alignment = self.alignment_center
        ws2 = self.insert_into_cell(ws2, 'C', '2', u'Наименование предприятия')
        ws2['C2'].alignment = self.alignment_center
        ws2 = self.insert_into_cell(ws2, 'D', '2', u'Вид документа')
        ws2['D2'].alignment = self.alignment_center
        ws2 = self.insert_into_cell(ws2, 'E', '2', u'№')
        ws2['E2'].alignment = self.alignment_center
        ws2 = self.insert_into_cell(ws2, 'F', '2', u'Дата')
        ws2['F2'].alignment = self.alignment_center
        ws2 = self.insert_into_cell(ws2, 'G', '2', u'Приложение')
        ws2['G2'].alignment = self.alignment_center
        ws2 = self.insert_into_cell(ws2, 'H', '2', u'Сумма, тенге')
        ws2['H2'].alignment = self.alignment_center

        use_of_budget_doc = report.use_of_budget_doc
        init_row = 3
        '''
            item.cost_name
            item.id
        '''
        for item in use_of_budget_doc.items.all():
            end_row = init_row
            ws2 = self.insert_into_cell(ws2, 'A', init_row, item.id)
            ws2 = self.insert_into_cell(ws2, 'B', init_row, item.cost_name)
            for cost in item.costs.all():
                cost_init_row = end_row
                ws2 = self.insert_into_cell(ws2, 'H', cost_init_row, str(cost.costs))
                ws2 = self.insert_into_cell(ws2, 'C', cost_init_row, cost.budget_item.project.organization_details.name)
                for gp_doc in cost.gp_docs.all():
                    ws2 = self.insert_into_cell(ws2, 'D', end_row, gp_doc.document.get_status_cap())
                    ws2 = self.insert_into_cell(ws2, 'F', end_row, gp_doc.document.date_created.date().__str__())
                    ws2 = self.insert_into_cell(ws2, 'E', end_row, gp_doc.id)
                    end_row += 1
                # ws2.merge_cells("H{}:H{}".format(str(cost_init_row), str(end_row)))
            # ws2.merge_cells("A{}:A{}".format(str(init_row), str(end_row)))
            # ws2.merge_cells("B{}:B{}".format(str(init_row), str(end_row)))
            init_row = end_row

        ws3 = wb.create_sheet()
        ws3.title = u'Затраты'

        ws3 = self.insert_into_cell(ws3, 'A', '1', u"№ п/п")
        ws3 = self.insert_into_cell(ws3, 'B', '1', u"Наименование статей затрат по смете")
        ws3 = self.insert_into_cell(ws3, 'C', '1', u"Сумма бюджетных средств по смете")
        ws3 = self.insert_into_cell(ws3, 'D', '1', u"Израсходованная сумма")
        ws3 = self.insert_into_cell(ws3, 'E', '1', u"Остаток средств")
        ws3 = self.insert_into_cell(ws3, 'F', '1', u"Наименование подтверждающих документов")
        ws3 = self.insert_into_cell(ws3, 'G', '1', u"Примечание")

        row = 2
        for item in use_of_budget_doc.items.all():
            ws3 = self.insert_into_cell(ws3, 'A', row, item.id)
            ws3 = self.insert_into_cell(ws3, 'B', row, item.cost_type.name)
            milestone_costs = item.milestone.factmilestonecostrow_set.all()
            budget_sum = 0
            for milestone_cost in milestone_costs:
                budget_sum += milestone_cost.costs.amount
            ws3 = self.insert_into_cell(ws3, 'C', row, str(budget_sum))
            ws3 = self.insert_into_cell(ws3, 'D', row, str(item.total_expense.amount))
            ws3 = self.insert_into_cell(ws3, 'E', row, str(budget_sum - item.total_expense.amount))
            ws3 = self.insert_into_cell(ws3, 'F', row, item.documents[0].document.get_status_cap())
            ws3 = self.insert_into_cell(ws3, 'G', row, item.notes)
            row += 1

        filename = EXCEL_REPORTS_DIR+'/'+u'Отчет '+str(project.aggreement.document.number)+'.xlsx'
        wb.save(filename)
        return filename

