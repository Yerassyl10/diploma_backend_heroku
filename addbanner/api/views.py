from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from addbanner.models import AddModel
from addbanner.api.serializers import AddBannerSerializer


class AddsBannerListAPIView(APIView):
    def get(self, request):
        adds = AddModel.objects.all()
        serializer = AddBannerSerializer(adds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddBannerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'DELETE', 'GET'])
def add_banner_view(request, add_id):
    try:
        add = AddModel.objects.get(pk=add_id)
    except AddModel.DoesNotExist as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        serializer = AddBannerSerializer(add)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        add.delete()
        return Response({'deleted': True})

    elif request.method == 'PUT':
        serializer = AddBannerSerializer(instance=add, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors})
