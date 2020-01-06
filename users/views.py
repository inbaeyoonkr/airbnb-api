from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import ReadUserSerializer, WriteUserSerializer


class MeView(APIView):
    """ Me View Definition"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            ReadUserSerializer(request.user).data, status=status.HTTP_200_OK
        )

    def put(self, request):
        serializer = WriteUserSerializer(request.user, request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(ReadUserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        print(user)
        return Response(ReadUserSerializer(user).data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
