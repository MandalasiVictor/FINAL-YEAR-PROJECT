from django.urls import path
from .views import DashboardListView


urlpatterns = [
    path('home', DashboardListView.as_view(), name="dashboard"),
]
