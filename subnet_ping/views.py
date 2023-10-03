from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework import status, parsers
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .tasks import ping_task
from .models import SubnetPingInfo
from .utils import check_ip_subnet_is_valid
from .serializers import SubnetPingRegistrySerializer, SubnetPingResultRetrieverSerializer

# Create your views here.


class SubnetPingRegistryViewSet(APIView):
    parser_classes = [parsers.FormParser]

    @extend_schema(
        summary="Subnet Ping Background Task Registry",
        request=SubnetPingRegistrySerializer,
        responses={
            200: OpenApiResponse(description="Json Response"),
            400: OpenApiResponse(description="Validation Error."),
        },
    )
    def post(self, request):
        serializer = SubnetPingRegistrySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)

        is_valid_ip_message = check_ip_subnet_is_valid(
            ip=serializer.validated_data["ip"],
            subnet_mask=serializer.validated_data["subnet_mask"],
        )
        if is_valid_ip_message is not None:
            return Response(
                {"errors": is_valid_ip_message}, status.HTTP_400_BAD_REQUEST
            )

        task = ping_task.apply_async(
            kwargs={
                "ip": serializer.validated_data["ip"],
                "subnet_mask": serializer.validated_data["subnet_mask"],
            }
        )
        return Response(
            {"message": "Celery task started.", "task_id": task.task_id},
            status=status.HTTP_200_OK,
        )


class SubnetPingResultRetrieverViewSet(APIView):
    parser_classes = [parsers.FormParser]

    @extend_schema(
        summary="Subnet Ping Result Retriever",
        request=SubnetPingResultRetrieverSerializer,
        responses={
            200: OpenApiResponse(description="Json Response"),
            400: OpenApiResponse(description="Validation Error."),
        },
    )
    def post(self, request):
        serializer = SubnetPingResultRetrieverSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)

        start = serializer.validated_data["start"]
        per_page = serializer.validated_data["per_page"]
        ip_subnet_mask = serializer.validated_data["ip_subnet_mask"]

        results = cache.get(ip_subnet_mask)
        if results is not None:
            return Response(
                {
                    "start": start,
                    "per_page": per_page,
                    "total": len(results),
                    "results": results[start:start+per_page]
                }
            )

        results = []
        total = SubnetPingInfo.objects.count()
        for orm_model in SubnetPingInfo.objects.all()[start:start+per_page]:
            converted_record = orm_model.__dict__
            del converted_record["id"]
            del converted_record["_state"]

            results.append(converted_record)

        return Response(
            {
                "start": start,
                "per_page": per_page,
                "total": total,
                "results": results
            }
        )



