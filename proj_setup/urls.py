from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from qualis.views.api_view import JournalViewSet
from qualis.views import *

router = routers.DefaultRouter()
router.register('journals', JournalViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('importa_arquivo', import_view.import_file, name='importa_arquivo'),
]
