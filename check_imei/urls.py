from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from django.urls import path, include
from account.views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include_docs_urls(title='API docs')),
    path('users/user/', include('account.urls', namespace='user')),
    path('check/', include('api.urls', namespace='check')),
    path('auth/token/create/', MyTokenObtainPairView.as_view(), name='token_auth'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
