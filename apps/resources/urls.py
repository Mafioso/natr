from rest_framework.routers import DefaultRouter
from .project import ProjectViewSet
from .document import DocumentViewSet


router = DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'projects', ProjectViewSet)


urlpatterns = router.urls
