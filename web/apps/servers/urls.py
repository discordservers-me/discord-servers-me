from django.urls import path

from . import views

app_name = 'server'

urlpatterns = [
    path('<int:server_id>', views.ServerDetailView.as_view(), name='detail'),
    path('<int:server_id>/update', views.ServerUpdateView.as_view(), name='update'),
    path('top-100', views.ServerTop100ListView.as_view(), name='list_top_100'),
    path('tag/<str:tag>', views.ServerTagListView.as_view(), name='list_tag'),
    path('search', views.ServerSearchListView.as_view(), name='search'),


]
