from rest_framework.routers import DefaultRouter
from .project import ProjectViewSet


router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = router.urls
