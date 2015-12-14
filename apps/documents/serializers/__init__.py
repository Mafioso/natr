#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .budget_report import (
    FactMilestoneCostRowSerializer,
    GPDocumentSerializer,
    UseOfBudgetDocumentItemSerializer,
    UseOfBudgetDocumentSerializer)
from .cost import (
    MilestoneCostRowSerializer,
    MilestoneCostCellSerializer,
    MilestoneFundingRowSerializer,
    MilestoneFundingCellSerializer,
    CostDocumentSerializer)
from .misc import (
    DocumentSerializer,
    DocumentCompositionSerializer,
    AgreementDocumentSerializer,
    OtherAgreementsDocumentSerializer,
    OtherAgreementItemSerializer,
    BasicProjectPasportSerializer,
    ProjectTeamMemberSerializer,
    DevelopersInfoSerializer,
    TechnologyCharacteristicsSerializer,
    IntellectualPropertyAssesmentSerializer,
    TechnologyReadinessSerializer,
    InnovativeProjectPasportSerializer,
    StatementDocumentSerializer,
    CalendarPlanItemSerializer,
    CalendarPlanDocumentSerializer,
    ProjectStartDescriptionSerializer,
    AttachmentSerializer)


budget_classes = (
    FactMilestoneCostRowSerializer,
    GPDocumentSerializer,
    UseOfBudgetDocumentItemSerializer,
    UseOfBudgetDocumentSerializer)
cost = (
    MilestoneCostRowSerializer,
    MilestoneCostCellSerializer,
    MilestoneFundingRowSerializer,
    MilestoneFundingCellSerializer,
    CostDocumentSerializer)
misc = (
    DocumentSerializer,
    DocumentCompositionSerializer,
    AgreementDocumentSerializer,
    OtherAgreementsDocumentSerializer,
    OtherAgreementItemSerializer,
    BasicProjectPasportSerializer,
    ProjectTeamMemberSerializer,
    DevelopersInfoSerializer,
    TechnologyCharacteristicsSerializer,
    IntellectualPropertyAssesmentSerializer,
    TechnologyReadinessSerializer,
    InnovativeProjectPasportSerializer,
    StatementDocumentSerializer,
    CalendarPlanItemSerializer,
    CalendarPlanDocumentSerializer,
    ProjectStartDescriptionSerializer,
    AttachmentSerializer)

__all__ = map(lambda x: x.__name__, budget_classes + cost + misc)