from rest_framework import serializers

from .models import Publisher


class PublisherSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Publisher.objects.create(**validated_data)

    class Meta:
        model = Publisher
        fields = ["id", "name"]

        read_only_fields = ["id"]
