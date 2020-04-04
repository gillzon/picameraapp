from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView



app_name = 'core'

urlpatterns = [
	path('',LoginView.as_view(),name='login'),
	path('add_plant/',views.Create_Plant.as_view(),name='add_plant'),
	path('loggedin/',views.LoggedIn.as_view(),name='loggedin'),
	path('upload_photo/<int:pk>/',views.UploadPhoto.as_view(),name='upload_photo'),
	path('<int:pk>/delete/', views.Delete_Plant_View.as_view(), name='delete_plant'),
]
