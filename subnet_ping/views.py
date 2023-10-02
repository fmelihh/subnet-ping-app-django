from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .tasks import counter_task
from .serializers import SubnetPingSerializers

# Create your views here.


class SubnetPingViewSet(APIView):
    parser_classes = [parsers.FormParser]

    @extend_schema(
        summary="Subnet Ping",
        request=SubnetPingSerializers,
        responses={
            200: OpenApiResponse(description="Json Response"),
            400: OpenApiResponse(description="Validation Error."),
        },
    )
    def post(self, request):
        serializer = SubnetPingSerializers()
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status.HTTP_400_BAD_REQUEST)
