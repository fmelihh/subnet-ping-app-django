from django.urls import path

from subnet_ping import views

urlpatterns = [
 path('subnet-ping', views.SubnetPingViewSet.as_view(), name='subnet_ping'),
]