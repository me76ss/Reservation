from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProgramList.as_view(), name='program'),
    path('<int:pk>', views.ProgramDetail.as_view(), name='program-detail'),
]
