from rest_framework import serializers


class SubnetPingRegistrySerializer(serializers.Serializer):
    ip = serializers.IPAddressField(required=True)
    subnet_mask = serializers.IntegerField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class SubnetPingResultRetrieverSerializer(serializers.Serializer):
    ip_subnet_mask = serializers.CharField()
    start = serializers.IntegerField(default=0)
    per_page = serializers.IntegerField(default=10)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
