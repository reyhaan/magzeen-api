from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views.userView import UserView

router = DefaultRouter()
router.register('user', UserView, base_name='test-set')

urlpatterns = [
    url(r'', include(router.urls))
]