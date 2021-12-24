from addbanner.models import AddModel
from rest_framework import serializers

class AddBannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddModel
        fields = '__all__'