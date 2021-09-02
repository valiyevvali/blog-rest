from rest_framework.generics import ( CreateAPIView,
                                      ListAPIView,
                                      DestroyAPIView,
                                      UpdateAPIView,
                                      RetrieveUpdateAPIView)
from comment.models import Comment
from .serializers import (CommentCreateSerializer,
                          CommentListSerializer,
                          CommentDeleteUpdateSerializer,)
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


class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [Isowner,]


class CommentUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [Isowner, ]

