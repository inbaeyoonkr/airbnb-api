from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer


class ListRoomsView(ListAPIView):
    """ List Rooms View Definition """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

