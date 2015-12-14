from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url
from .project import ProjectViewSet, MonitoringTodoViewSet, MonitoringViewSet, ReportViewSet, MilestoneViewSet
from .document import (
	DocumentViewSet, 
	BasicProjectPasportDocumentViewSet,
	InnovativeProjectPasportDocumentViewSet,
	CalendarPlanDocumentViewSet, 
	ProjectStartDescriptionViewSet,
	AttachmentViewSet, 
	UseOfBudgetDocumentViewSet,
	CostDocumentViewSet,
	CostTypeViewSet,
	FactMilestoneCostRowViewSet
)
from .journal import JournalActivityViewSet, JournalViewSet
from .notification import NotificationViewSet, NotificationSubscriptionViewSet, NotificationCounterViewSet
from .user import get_current_user

router = DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'calendar-plans', CalendarPlanDocumentViewSet, 'calendarplan')
router.register(r'projects', ProjectViewSet)
router.register(r'milestones', MilestoneViewSet, 'milestone')
router.register(r'reports', ReportViewSet)
router.register(r'attachments', AttachmentViewSet, 'attachment')
router.register(r'use_of_budget', UseOfBudgetDocumentViewSet, 'use_of_budget')
router.register(r'basic_pasport', BasicProjectPasportDocumentViewSet, 'basic_pasport')
router.register(r'cost_documents', CostDocumentViewSet, 'costdocument')
router.register(r'innovative_pasport', InnovativeProjectPasportDocumentViewSet, 'innovative_pasport')
router.register(r'monitoring', MonitoringViewSet, 'monitoring')
router.register(r'start_description', ProjectStartDescriptionViewSet, 'start_description')
router.register(r'cost_types', CostTypeViewSet, 'cost_types')
router.register(r'cost_row', FactMilestoneCostRowViewSet, 'cost_row')

monitoring_router = routers.NestedSimpleRouter(router, r'monitoring', lookup='monitoring')
monitoring_router.register(r'todos', MonitoringTodoViewSet, base_name='monitoring-todos')
# router.register(r'todo', MonitoringTodoViewSet, 'monitoring')

router.register(r'journals', JournalViewSet, 'journal')
router.register(r'journal/activities', JournalActivityViewSet, 'activity')
router.register(r'notifications', NotificationViewSet, 'notification')
router.register(r'my-notifications', NotificationSubscriptionViewSet, 'notif_subscription')
router.register(r'notif-counter', NotificationCounterViewSet, 'notif_counter')

urlpatterns = [
	url(r'', include(router.urls)),
	url(r'', include(monitoring_router.urls)),
	url(r'current-user/$', get_current_user)
]
