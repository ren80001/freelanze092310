from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('register.urls')),
    path('auth/', include('social_django.urls', namespace='social')),  # <- Here

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)