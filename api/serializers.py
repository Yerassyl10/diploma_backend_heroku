from rest_framework import serializers
from api.models import Company, Opportunity


class CompanySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    picture = serializers.ImageField()
    about_company = serializers.CharField()
    read_more = serializers.CharField()

    def create(self, validated_data):
        company = Company.objects.create(name=validated_data.get('name'))
        return company

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class OpportunitySerializer(serializers.ModelSerializer):
    # category = CategorySerializer2(read_only=True)
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Opportunity
        fields = '__all__'
