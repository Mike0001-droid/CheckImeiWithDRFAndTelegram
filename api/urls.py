from rest_framework import routers
from api import views

router = routers.DefaultRouter()

router.register(r'', views.CheckImeiViewSet, basename='check_imei')

app_name = 'api'
urlpatterns = router.urls



