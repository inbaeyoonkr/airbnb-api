import jwt
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .models import User
from rooms.models import Room
from rooms.serializers import RoomSerializer
from .serializers import UserSerializer
from .permissions import IsSelf


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        elif (
            self.action == "create"
            or self.action == "retrieve"
            or self.action == "favs"
        ):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                encoded_jwt = jwt.encode(
                    {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
                )
                return Response(data={"token": encoded_jwt, "id": user.pk})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True)
    def favs(self, request, pk):
        user = self.get_object()
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    @favs.mapping.put
    def toggle_favs(self, request, pk):
        user = User.objects.get(pk=pk)
        pk = request.data.get("pk", None)
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)
