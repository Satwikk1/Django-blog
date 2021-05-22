from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='form-home'),
	path('children/<int:parent_id>/', views.manage_children, name='manage_children')
]