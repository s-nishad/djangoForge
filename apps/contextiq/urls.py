from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DocumentQueryAPIView

app_name = 'contextiq'

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path("query/", DocumentQueryAPIView.as_view(), name="document-query"),
    path('', include(router.urls)),
]
