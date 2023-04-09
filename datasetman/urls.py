from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('upload_dataset/', views.UploadDatasetView.as_view(), name='upload-dataset'),
    path('dataset/<str:dataset_id>/', views.DatasetDetailView.as_view(), name='detail-dataset'),
    path('dataset/download/<str:dataset_id>/', views.download_dataset, name='download-dataset'),
    path('dataset/clone/<str:dataset_id>/', views.clone_dataset, name="clone-dataset"),
    path('dataset/comment/<str:dataset_id>/', views.comment_dataset, name="comment-dataset"),
    path('dataset/comment/reply/<str:comment_id>/', views.reply_comment, name='reply-comment-dataset'),
]
