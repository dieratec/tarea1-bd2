from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('upload_dataset', views.UploadDatasetView.as_view(), name='upload-dataset'),
]
