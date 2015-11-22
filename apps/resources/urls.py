from rest_framework.routers import DefaultRouter
from .project import ProjectViewSet
from .document import DocumentViewSet, CalendarPlanDocumentViewSet


router = DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'calendar-plans', CalendarPlanDocumentViewSet, 'calendarplan')
router.register(r'projects', ProjectViewSet)


urlpatterns = router.urls
