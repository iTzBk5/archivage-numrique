
from django.contrib import admin
from django.urls import path, include
from search.views import search_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', search_view),
    path('', include('blog.urls')),
    
]
from django.conf.urls.static import static
from django.conf import settings
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)