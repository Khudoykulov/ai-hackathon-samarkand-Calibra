from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIAnalysisViewSet, AIModelViewSet, AILearningDataViewSet

router = DefaultRouter()
router.register(r'analysis', AIAnalysisViewSet)
router.register(r'models', AIModelViewSet)
router.register(r'learning', AILearningDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
