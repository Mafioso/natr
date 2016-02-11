#!/usr/bin/env python
# -*- coding: utf-8 -*-
from natr.settings import EXCEL_REPORTS_DIR
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side, Color, colors, PatternFill
from openpyxl.cell import get_column_letter
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
import decimal
import os


class ExcelReport:
    assignments = []
    assig_intervals = [
        u'Никогда',
        u'Еженедельно',
        u'Ежемесячно',
        u'Ежеквартально',
        u'Каждые полгода',
        u'Ежегодно'
    ]
    assig_statuses =  [
        u'Не назначено',
        u'Назначено',
        u'Отправлено на доработку',
        u'Исполнение продолжается',
        u'На утверждении',
        u'Утверждено',
        u'Исполнено'
    ]
    alignment_left=Alignment(horizontal='left',
                    vertical='top',
                    text_rotation=0,
                    wrap_text=True,
                    shrink_to_fit=False,
                    indent=0)
    alignment_right=Alignment(horizontal='right',
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

    greyFill = PatternFill(start_color='B3B3B3',
                   end_color='B3B3B3',
                   fill_type='solid')

    def __init__(self, report=None, projects=None, registry_data = None):
        self.report = report
        self.projects = projects
        self.registry_data = registry_data

    def build_header_cell(self, ws, column, cell_number, string):
        ws = self.insert_into_cell(ws, column, cell_number, string)
        ws.alignment = self.alignment_center
        ws.font = Font(bold=True)
        return ws

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
        try:
            ws1 = self.insert_into_cell(ws1, 'B', '2', project.organization_details.name)
        except:
            ws1 = self.insert_into_cell(ws1, 'B', '2', "")
        contract_number_date = "{0}, {1}".format(project.aggreement.document.number, project.aggreement.document.date_sign) if project is not None else ""
        ws1 = self.insert_into_cell(ws1, 'B', '3', contract_number_date)
        ws1 = self.insert_into_cell(ws1, 'B', '4', project.grant_goal if project is not None else "")
        try:
            ws1 = self.insert_into_cell(ws1, 'B', '5', "{0} {1}".format(milestone.fundings.amount, milestone.fundings.currency))
        except:
            ws1 = self.insert_into_cell(ws1, 'B', '5', "")
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
            try:
                ws3 = self.insert_into_cell(ws3, 'F', row, item.documents[0].document.get_status_cap())
            except:
                ws3 = self.insert_into_cell(ws3, 'F', row, str(0))
            ws3 = self.insert_into_cell(ws3, 'G', row, item.notes)
            row += 1
        file_dir = EXCEL_REPORTS_DIR
        if not os.path.exists(EXCEL_REPORTS_DIR):
            os.makedirs(EXCEL_REPORTS_DIR)
        filename = EXCEL_REPORTS_DIR + '/' + u'Отчет ' + str(project.aggreement.document.number) + '.xlsx'
        wb.save(filename)
        return filename

    def generate_experts_report(self):
        projects = self.projects
        max_milestone_num = 0
        for project in projects:
            if len(project.milestone_set.all())>max_milestone_num:
                max_milestone_num = len(project.milestone_set.all())

        wb = Workbook()
        ws = wb.active

        if len(projects) == 0:
            ws = self.insert_into_cell(ws, 'A', '1', u'Реестр проектов')
            ws = self.insert_into_cell(ws, 'A', '2', u'Проектов не найдено')
            ws.merge_cells('A1:B1')
            ws['A1'].alignment = self.alignment_center
            ws['A1'].font = Font(bold=True)

            file_dir = EXCEL_REPORTS_DIR
            if not os.path.exists(EXCEL_REPORTS_DIR):
                os.makedirs(EXCEL_REPORTS_DIR)

            filename = EXCEL_REPORTS_DIR+'/'+u'Отчет по грантам.xlsx'
            wb.save(filename)
            return filename

        all_cols_number = 0
        temp_col_num = 0
        first = True
        p_len = 0
        row = 1

        if type(projects) == list:
            p_len = len(projects)
        elif type(projects) == QuerySet:
            p_len = projects.count()

        for project, cnt in zip( self.projects, range(p_len) ):
            col_num = 1
            row = cnt+4
            if first:
                ws = self.build_header_cell(ws, get_column_letter(col_num), row-1, u'№ п/п' )

            ws = self.insert_into_cell(ws, get_column_letter(col_num), row, str(cnt+1))

            col_num += 1

            if 'aggreement' in self.registry_data['keys']:
                if first:
                    ws = self.build_header_cell(ws, get_column_letter(col_num), row-1, u'№/дата договора' )

                if project.aggreement: 
                    agreement_number = project.aggreement.document.number if project.aggreement.document.number else ""
                else:
                    agreement_number = ""

                if project.aggreement and project.aggreement.document.date_sign:
                    agreement_date = u' от ' + project.aggreement.document.date_sign.strftime("%d.%m.%y")
                else:
                    agreement_date = ""
                ws = self.insert_into_cell(ws, get_column_letter(col_num), row, agreement_number + agreement_date)
                
                col_num += 1
                
            if 'grantee_name' in self.registry_data['keys']:
                if first:
                    ws = self.build_header_cell(ws, get_column_letter(col_num), row-1, u'Наименование Грантополучателя' )
                try:
                    ws = self.insert_into_cell(ws, get_column_letter(col_num), row, project.organization_details.name)
                except ObjectDoesNotExist:
                    ws = self.insert_into_cell(ws, get_column_letter(col_num), row, '')
                col_num += 1

            if 'project_name' in self.registry_data['keys']:
                if first:
                    ws = self.build_header_cell(ws, get_column_letter(col_num), row-1, u'Наименование проекта')
                ws = self.insert_into_cell(ws, get_column_letter(col_num), row, project.name) 
                col_num += 1

            if 'grant_type' in self.registry_data['keys']:
                if first:
                    ws = self.build_header_cell(ws, get_column_letter(col_num), row-1, u'Вид гранта' )
                if project.funding_type:
                    ws = self.insert_into_cell(ws, get_column_letter(col_num), row, project.funding_type.get_name_display())
                col_num += 1

            if 'region' in self.registry_data['keys']:
                if first:
                    ws = self.build_header_cell(ws, get_column_letter(col_num), row-1, u'Регион' )
                col_num += 1

            if 'total_month' in self.registry_data['keys']:
                if first:
                    ws = self.build_header_cell(ws, get_column_letter(col_num), row-1, u'Срок реализации проекта, (мес)' )
                ws = self.insert_into_cell(ws, get_column_letter(col_num), row, project.total_month)
                col_num += 1

            if 'fundings' in self.registry_data['keys']:
                if first:
                    ws = self.build_header_cell(ws, get_column_letter(col_num), row-1, u'Сумма по Договору, (тенге)')
                sum_fundings = 0
                if project.fundings:
                    sum_fundings += project.fundings.amount
                if project.own_fundings:
                    sum_fundings += project.own_fundings.amount
                ws = self.insert_into_cell(ws, get_column_letter(col_num), row, str(sum_fundings))
                col_num += 1


            money_sum = 0
            temp_col_num = col_num
            for milestone in project.milestone_set.all():
                if milestone.fundings:
                    money_sum += milestone.fundings.amount

                if 'transhes' in self.registry_data['keys']: 
                    try:
                        ws = self.insert_into_cell(ws, greyFillet_column_letter(col_num), row, str(project.milestone_set.all()[i-10].fundings.amount))
                    except:
                        ws = self.insert_into_cell(ws, get_column_letter(col_num), row, str(0))
                    col_num += 1
            
            if 'transhes' in self.registry_data['keys']: 
                if first:
                    for i in range(col_num, col_num+max_milestone_num):
                        ws = self.build_header_cell(ws, get_column_letter(i), row-1, u'{} транш'.format(str(i-col_num+1)) )
                col_num = temp_col_num + max_milestone_num    
                
            if 'expert' in self.registry_data['keys']:
                if first:
                    ws = self.build_header_cell(ws, get_column_letter(col_num), row-1, u'Исполнитель' )
                assigned_experts = []

                for expert in project.assigned_experts.all():
                    assigned_experts.append(expert.get_full_name())

                ws = self.build_header_cell( ws, get_column_letter(col_num), row, ",".join(assigned_experts) )
                col_num += 1

            if 'balance' in self.registry_data['keys']:
                if first:
                    ws = self.build_header_cell(ws, get_column_letter(col_num), row-1, u'Остаток денежных средств,  (тенге)' )
                if not project.fundings:
                    ws = self.insert_into_cell(ws, get_column_letter(col_num), row, str(0))
                else:
                    ws = self.insert_into_cell(ws, get_column_letter(col_num), row, str(project.fundings.amount - money_sum))
                col_num += 1

            if 'status' in self.registry_data['keys']:
                if first:
                    ws = self.build_header_cell(ws, get_column_letter(col_num), row-1, u'Статус ' )     
                ws = self.insert_into_cell(ws, get_column_letter(col_num), row, project.get_status_cap())               
                col_num += 1

            if 'total_fundings' in self.registry_data['keys']:
                if first:
                    ws = self.build_header_cell(ws, get_column_letter(col_num), row-1, u'Итого перечислено')
                ws = self.insert_into_cell(ws, get_column_letter(col_num), row, str(money_sum))
                col_num += 1

            all_cols_number = col_num
            first = False

        ws = self.insert_into_cell(ws, 'A', '1', u'Отчет по грантам')
        ws.merge_cells('A1:%s1'%get_column_letter(all_cols_number-1 if all_cols_number > 1 else 1))
        ws['A1'].alignment = self.alignment_center
        ws['A1'].font = Font(bold=True)

        row += 2
        ws = self.insert_into_cell(ws, 'A', row, u'Итого по договорам на мониторинге ')
        ws.merge_cells("A%s:%s%s"%(row, get_column_letter(all_cols_number-1 if all_cols_number > 1 else 1), row))
        ws["A{}".format(row)].alignment = self.alignment_center
        row += 1

        ws = self.insert_into_cell(ws, 'A', row, u'ВСЕГО по Договорам 2015 года:')
        ws.merge_cells("A%s:%s%s"%(row, get_column_letter(temp_col_num-2 if temp_col_num > 2 else 1), row))
        ws["A{}".format(row)].alignment = self.alignment_right

        if temp_col_num > 2 and all_cols_number > 2:
            for i in range(temp_col_num-1, all_cols_number):
                sum = 0
                for j in range(2, row-1):
                    val = ws['{}{}'.format(get_column_letter(i), j)].value
                    try:                 
                        sum += decimal.Decimal(val)
                    except:
                        pass
                ws = self.insert_into_cell(ws, get_column_letter(i), row, str(sum))

        for i in range(all_cols_number):
            ws.column_dimensions[get_column_letter(i+1)].width = 20.0

        file_dir = EXCEL_REPORTS_DIR
        if not os.path.exists(EXCEL_REPORTS_DIR):
            os.makedirs(EXCEL_REPORTS_DIR)

        filename = EXCEL_REPORTS_DIR+'/'+u'Отчет по грантам 2015 года.xlsx'

        if 'date_from' in self.registry_data and "date_to" in self.registry_data:
            dates = self.registry_data['date_from'].strftime("%d.%m.%y") + \
                    "-" + self.registry_data['date_to'].strftime("%d.%m.%y")
            
            ws = self.insert_into_cell(ws, 'A', '1', u'Реестр проектов ' + dates)
            ws.merge_cells('A1:%s1'%get_column_letter(all_cols_number-1 if all_cols_number > 1 else 1))
            ws['A1'].alignment = self.alignment_center
            ws['A1'].font = Font(bold=True)

            ws = self.insert_into_cell(ws, 'A', row, u'ВСЕГО по Договорам ' + dates)
            ws.merge_cells("A%s:%s%s"%(row, get_column_letter(temp_col_num-2 if temp_col_num > 2 else 1), row))
            ws["A{}".format(row)].alignment = self.alignment_right

            filename = EXCEL_REPORTS_DIR + '/' + u'Реестр проектов ' + dates + '.xlsx'

        wb.save(filename)
        return filename

