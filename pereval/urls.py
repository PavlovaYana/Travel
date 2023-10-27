from django.urls import path, include
from .views import PerevalViewSet, EmailAPIView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'pereval', PerevalViewSet, basename='pereval')

urlpatterns = [
    path('submitData/', include(router.urls)),
    path('submitData/user__email=<str:email>', EmailAPIView.as_view())
]