#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openpyxl import Workbook
from natr.settings import EXCEL_REPORTS_DIR

def generate_excel_file(report):
    project = report.project
    milestone = report.milestone
    wb = Workbook()
    ws1 = wb.active
    ws1.title = u'Общая информация'

    ws1 = insert_into_cell(ws1, 'A', '1', u'Дата отчета')
    ws1 = insert_into_cell(ws1, 'A', '2', u'Наименование грантополучателя')
    ws1 = insert_into_cell(ws1, 'A', '3', u'Номер и дата договора')
    ws1 = insert_into_cell(ws1, 'A', '4', u'Цель гранта')
    ws1 = insert_into_cell(ws1, 'A', '5', u'Сумма гранта')
    ws1 = insert_into_cell(ws1, 'A', '6', u'Период отчетности')
    ws1 = insert_into_cell(ws1, 'A', '7', u'Достигнутые результаты грантового проекта')
    ws1 = insert_into_cell(ws1, 'A', '8', u'Наименование охранного документа (в случае наличия)')
    ws1 = insert_into_cell(ws1, 'A', '9', u'Номер и дата выдачи охранного документа (в случае наличия)')

    ws1 = insert_into_cell(ws1, 'B', '1', report.date)
    ws1 = insert_into_cell(ws1, 'B', '2', project.organization_details.name if project is not None else "")
    ws1 = insert_into_cell(ws1, 'B', '3', "{0}, {1}".format(project.aggreement.document.number, project.aggreement.document.date_sign) if project is not None else "")
    ws1 = insert_into_cell(ws1, 'B', '4', project.grant_goal if project is not None else "")
    ws1 = insert_into_cell(ws1, 'B', '5', "{0} {1}".format(milestone.fundings.amount, milestone.fundings.currency) if milestone is not None else "")
    ws1 = insert_into_cell(ws1, 'B', '6', report.period if project is not None else "")
    ws1 = insert_into_cell(ws1, 'B', '7', report.results if project is not None else "")



    ws2 = wb.create_sheet()
    ws2.title = u'Бюждетные средства'

    ws2 = insert_into_cell(ws2, 'A', '1', u'Номер п/п')
    ws2 = insert_into_cell(ws2, 'B', '1', u'Статьи затрат по договору')
    ws2 = insert_into_cell(ws2, 'C', '1', u'Документы по отчету грантополучателя за Этап № {0}'.format(milestone.number))
    ws2 = insert_into_cell(ws2, 'D', '1', "")
    ws2 = insert_into_cell(ws2, 'E', '1', "")
    ws2 = insert_into_cell(ws2, 'F', '1', "")
    ws2 = insert_into_cell(ws2, 'G', '1', "")
    ws2 = insert_into_cell(ws2, 'H', '1', "")
    ws2.merge_cells('C1:H1')
    ws2.merge_cells('A1:A2')
    ws2.merge_cells('B1:B2')
    ws2 = insert_into_cell(ws2, 'C', '2', u'Наименование предприятия,')
    ws2 = insert_into_cell(ws2, 'D', '2', u'Вид документа,')
    ws2 = insert_into_cell(ws2, 'E', '2', u'№,')
    ws2 = insert_into_cell(ws2, 'F', '2', u'Дата,')
    ws2 = insert_into_cell(ws2, 'G', '2', u'Приложение,')
    ws2 = insert_into_cell(ws2, 'H', '2', u'Сумма, тенге')

    use_of_budget_doc = report.use_of_budget_doc
    row = 3
    for item in user_of_budget_doc.items.all():
        pass



    filename = EXCEL_REPORTS_DIR+'/'+ws1.title+'.xlsx'
    wb.save(filename)
    return filename

def insert_into_cell(ws, column, cell_number, string):
    if not string:
        string = ""
    ws[column+cell_number] = string
    if ws.column_dimensions[column].width < len(string):
        ws.column_dimensions[column].width = len(string)
    return ws
