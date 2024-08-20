from .views import trade_API_view

urlpatterns = [
    path('trade-api/', trade_API_view, name='trade-api'),
]