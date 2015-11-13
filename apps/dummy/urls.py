from rest_framework.routers import DefaultRouter
from .dummy_api import DummyViewSet


router = DefaultRouter()
router.register(r'dummies', DummyViewSet, 'DummyClass')

urlpatterns = router.urls