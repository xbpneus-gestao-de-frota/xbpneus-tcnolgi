from django.urls import path
from .views import ExportJobApi, ExportJobStatusApi, ExportJobDownloadApi
urlpatterns = [
    path("export/", ExportJobApi.as_view()),
    path("<int:job_id>/", ExportJobStatusApi.as_view()),
    path("<int:job_id>/download/", ExportJobDownloadApi.as_view()),
]
