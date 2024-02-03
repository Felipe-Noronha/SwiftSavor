from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('recipes/', include('recipes.urls')),
    path('users/', include('users.urls')),
    path('ingredients/', include('ingredients.urls')),
    path('admin_tools/', include('admin_tools.urls')),
    path('favorites/', include('favorites.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
