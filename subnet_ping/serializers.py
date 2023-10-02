from rest_framework import serializers


class SubnetPingSerializers(serializers.Serializer):
    ip = serializers.IPAddressField(required=True)
    subnet_mask = serializers.IntegerField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
