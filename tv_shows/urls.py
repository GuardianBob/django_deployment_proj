from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('shows', views.shows),
    path('shows/new', views.new),
    path('shows/create', views.create),
    path('shows/<int:uid>', views.info),
    path('shows/<int:uid>/edit', views.edit),
    path('shows/<int:uid>/update', views.update),
    path('shows/<int:uid>/destroy', views.destroy),
    ]