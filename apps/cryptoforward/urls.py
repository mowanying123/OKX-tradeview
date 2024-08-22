from .views import trade_API_view
from django.urls import include, path

urlpatterns = [
    path('trade-api/', trade_API_view, name='trade-api'),
]