from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url
from .project import (
	ProjectViewSet,
	MonitoringTodoViewSet,
	MonitoringViewSet,
	ReportViewSet,
	MilestoneViewSet,
	CorollaryViewSet,
	RiskCategoryViewSet,
	RiskDefinitionViewSet,
	CommentViewSet
)
from .document import (
	DocumentViewSet,
	BasicProjectPasportDocumentViewSet,
	InnovativeProjectPasportDocumentViewSet,
	CalendarPlanDocumentViewSet,
	ProjectStartDescriptionViewSet,
	AttachmentViewSet,
	UseOfBudgetDocumentViewSet,
	UseOfBudgetDocumentItemViewSet,
	CostDocumentViewSet,
	CostTypeViewSet,
	FactMilestoneCostRowViewSet,
	GPDocimentViewSet,
	GPDocumentTypeViewSet,
	TechStageViewSet
)
from .journal import JournalActivityViewSet, JournalViewSet
from .notification import NotificationViewSet, NotificationSubscriptionViewSet, NotificationCounterViewSet
from .user import get_initial_state
from .natr_user import NatrUserViewSet, PermissionViewSet, GroupViewSet, DepartmentViewSet
from .grantee_user import GranteeUserViewSet


router = DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'calendar-plans', CalendarPlanDocumentViewSet, 'calendarplan')
router.register(r'projects', ProjectViewSet)
router.register(r'milestones', MilestoneViewSet, 'milestone')
router.register(r'reports', ReportViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'corollaries', CorollaryViewSet)
router.register(r'attachments', AttachmentViewSet, 'attachment')
router.register(r'use_of_budget', UseOfBudgetDocumentViewSet, 'use_of_budget')
router.register(r'use_of_budget_items', UseOfBudgetDocumentItemViewSet, 'use_of_budget')
router.register(r'basic_pasport', BasicProjectPasportDocumentViewSet, 'basic_pasport')
router.register(r'cost_documents', CostDocumentViewSet, 'costdocument')
router.register(r'innovative_pasport', InnovativeProjectPasportDocumentViewSet, 'innovative_pasport')
router.register(r'monitoring', MonitoringViewSet, 'monitoring')
router.register(r'start_description', ProjectStartDescriptionViewSet, 'start_description')
router.register(r'cost_types', CostTypeViewSet, 'cost_types')
router.register(r'cost_row', FactMilestoneCostRowViewSet, 'cost_row')
router.register(r'gp_docs', GPDocimentViewSet, 'gp_docs')
router.register(r'gp_doc_types', GPDocumentTypeViewSet, 'gp_doc_type')
router.register(r'risk_categories', RiskCategoryViewSet, 'risk_categories')
router.register(r'risks', RiskDefinitionViewSet, 'risk')
router.register(r'tech_stages', TechStageViewSet, 'tech_stages')
router.register(r'monitoring_todos', MonitoringTodoViewSet, 'monitoring_todos')

monitoring_router = routers.NestedSimpleRouter(router, r'monitoring', lookup='monitoring')
monitoring_router.register(r'todos', MonitoringTodoViewSet, base_name='monitoring-todos')
# router.register(r'todo', MonitoringTodoViewSet, 'monitoring')

router.register(r'journals', JournalViewSet, 'journal')
router.register(r'activities', JournalActivityViewSet, 'activity')
router.register(r'notifications', NotificationViewSet, 'notification')
router.register(r'my-notifications', NotificationSubscriptionViewSet, 'notif_subscription')
router.register(r'notif-counter', NotificationCounterViewSet, 'notif_counter')
router.register(r'natr-user', NatrUserViewSet, 'natr_user')
router.register(r'grantee-user', GranteeUserViewSet, 'grantee_user')
router.register(r'permissions', PermissionViewSet, 'permission')
router.register(r'groups', GroupViewSet, 'group')
router.register(r'departments', DepartmentViewSet, 'department')

urlpatterns = [
	url(r'', include(router.urls)),
	url(r'', include(monitoring_router.urls)),
	url(r'initial-state/$', get_initial_state)
]
