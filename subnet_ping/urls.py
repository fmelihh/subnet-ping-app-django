from django.urls import path

from subnet_ping import views

urlpatterns = [
    path(
        "subnet-ping-registry",
        views.SubnetPingRegistryViewSet.as_view(),
        name="subnet_ping_registry",
    ),
    path(
        "subnet-ping-result-retriever",
        views.SubnetPingResultRetrieverViewSet.as_view(),
        name="subnet_ping_result_retriever",
    ),
]
