from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProgramList.as_view(), name='program'),
    path('<int:pk>', views.ProgramDetail.as_view(), name='program-detail'),
    path('<int:pg_pk>/slots/<int:sl_pk>', views.ProgramSlotDetail.as_view(), name='program-slot'),
    path('reserves', views.UserReserveList.as_view(), name='user-reserve'),
    path('reserves/<int:pk>', views.UserReserveDetail.as_view(), name='user-reserve-detail'),
]
