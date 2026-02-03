from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_header = "PlannerFit Admin"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/plans/', include('plans.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
