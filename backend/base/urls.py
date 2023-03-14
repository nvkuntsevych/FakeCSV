from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from base import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('schemas/', include('schemas.urls')),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler400 = 'schemas.views.handler400'
handler403 = 'schemas.views.handler403'
handler404 = 'schemas.views.handler404'
handler500 = 'schemas.views.handler500'
