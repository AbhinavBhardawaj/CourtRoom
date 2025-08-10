from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('privacy/', views.privacy, name='privacy'),
    path('contact/', views.contact, name='contact'),
    path('users/', include('users.urls')),
    path('cases/', include('cases.urls')),                # ← Change: Modular include for all user routes
    path("__reload__/", include("django_browser_reload.urls")),  # Optional: dev hot reload
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
