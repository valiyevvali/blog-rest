from rest_framework.generics import ( CreateAPIView,
                                      ListAPIView,
                                      DestroyAPIView,
                                      UpdateAPIView,
                                      RetrieveAPIView)
from comment.models import Comment
from .serializers import (CommentCreateSerializer,
                          CommentListSerializer,
                          CommentDeleteUpdateSerializer,)

from rest_framework.mixins import DestroyModelMixin,CreateModelMixin
from .permissions import Isowner
from .paginations import CommentPagination

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)



class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = Comment.objects.filter(parent__isnull=True)
        query=self.request.GET.get('q')
        if query:
            queryset=queryset.filter(post=query)
        return queryset




# class CommentDeleteAPIView(DestroyAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentDeleteUpdateSerializer
#     lookup_field = 'pk'
#     permission_classes = [Isowner,]


#combine delete and update
class CommentUpdateAPIView(DestroyModelMixin,UpdateAPIView,RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [Isowner, ]

    def delete(self, request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


