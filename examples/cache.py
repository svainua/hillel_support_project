from rest_framework import serializers

from shared.cache import CacheService
from users.models import User


class ActivatorUserMetaSerializer(serializers.Serializer):
    id = serializers.IntegerField()


record: dict = CacheService().get(
    namespace="activation", key="a8d10fff-7849-33db-bf7a-e932be20369c"
)

serializer = ActivatorUserMetaSerializer(data=record)
serializer.is_valid(raise_exception=True)

serializer.validated_data["id"]

user = User.objects.get(id=instance.id)  # noqa
