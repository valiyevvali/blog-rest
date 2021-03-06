from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import FavouriteListCreateApiSerializer, FavouriteApiSerializer
from favourite.models import Favourite
from .paginations import FavouritePagination
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
class FavouriteListCreateAPIView(ListCreateAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteListCreateApiSerializer
    pagination_class = FavouritePagination
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavouriteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteApiSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner,]




