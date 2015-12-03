from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url
from .project import ProjectViewSet, MonitoringTodoViewSet, MonitoringViewSet, ReportViewSet
from .document import (
	DocumentViewSet, 
	BasicProjectPasportDocumentViewSet,
	CalendarPlanDocumentViewSet, 
	AttachmentViewSet, 
	UseOfBudgetDocumentViewSet
)
from .journal import JournalActivityViewSet, JournalViewSet

router = DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'calendar-plans', CalendarPlanDocumentViewSet, 'calendarplan')
router.register(r'projects', ProjectViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'attachments', AttachmentViewSet, 'attachment')
router.register(r'use_of_budget', UseOfBudgetDocumentViewSet, 'use_of_budget')
router.register(r'basic_pasport', BasicProjectPasportDocumentViewSet, 'basic_pasport')

router.register(r'monitoring', MonitoringViewSet, 'monitoring')

monitoring_router = routers.NestedSimpleRouter(router, r'monitoring', lookup='monitoring')
monitoring_router.register(r'todos', MonitoringTodoViewSet, base_name='monitoring-todos')
# router.register(r'todo', MonitoringTodoViewSet, 'monitoring')

router.register(r'journals', JournalViewSet, 'journal')
router.register(r'journal/activities', JournalActivityViewSet, 'activity')

urlpatterns = [
	url(r'', include(router.urls)),
	url(r'', include(monitoring_router.urls)),
]
