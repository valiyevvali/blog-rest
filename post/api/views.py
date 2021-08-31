from django.http import HttpResponse, JsonResponse
from rest_framework.generics import ( ListAPIView,
                                      RetrieveAPIView,
                                      DestroyAPIView,
                                      UpdateAPIView,
                                      CreateAPIView,
                                      RetrieveUpdateAPIView)

from post.api.permisions import IsOwner
from post.api.serializers import PostSerializer,PostCreateUpdateSerializer
from post.models import Post
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,IsAdminUser)
class PostListApiView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailApiView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


def post_detail(request, pk):
    # try:
    #     post = Post.objects.get(pk=pk)
    # except Post.DoesNotExist:
    #     return HttpResponse(status=404)
    post=get_object_or_404(Post,pk=pk)
    serializer = PostSerializer(post)
    return JsonResponse(serializer.data)

class PostDeleteApiView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

class PostUpdateApiView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

class PostCreateApiView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


