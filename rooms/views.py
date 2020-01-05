from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Room
from .serializers import RoomSerializer


class ListRoomsView(ListAPIView):
    """ List Rooms View Definition """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class SeeRoomView(RetrieveAPIView):
    """ See Room View Definition """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
