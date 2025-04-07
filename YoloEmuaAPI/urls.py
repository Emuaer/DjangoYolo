from django.urls import path
from .views import UploadImageView,UploadImageView_emua
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', UploadImageView_emua.as_view(), name='results'),
    path(r'media/(?P<path>.*)', serve,{'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)