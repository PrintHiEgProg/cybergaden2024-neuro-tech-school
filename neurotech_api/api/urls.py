from django.urls import path
from .views import CalibriListView, CalibriDetailView, CheckAuthView

urlpatterns = [
    path('', CalibriListView.as_view(), name='calibri-list'),
    path('calibri/', CalibriListView.as_view(), name='calibri-create'),
    path('calibri/<str:name>/', CalibriDetailView.as_view(), name='calibri-detail'),
    path('auth/check/', CheckAuthView.as_view(), name='check_auth'),
]
