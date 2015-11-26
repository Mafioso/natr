from rest_framework.routers import DefaultRouter
from .project import ProjectViewSet, MonitoringTodoViewSet, MonitoringViewSet, ReportViewSet
from .document import DocumentViewSet, CalendarPlanDocumentViewSet, AttachmentViewSet
from .journal import JournalActivityViewSet, JournalViewSet

router = DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'calendar-plans', CalendarPlanDocumentViewSet, 'calendarplan')
router.register(r'projects', ProjectViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'attachments', AttachmentViewSet, 'attachment')
router.register(r'monitoring', MonitoringViewSet, 'monitoring')
router.register(r'monitoring/todo', MonitoringTodoViewSet, 'monitoring')
router.register(r'journals', JournalViewSet, 'journal')
router.register(r'journal/activities', JournalActivityViewSet, 'activity')

urlpatterns = router.urls
