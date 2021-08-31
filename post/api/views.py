from django.http import HttpResponse, JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView,DestroyAPIView,UpdateAPIView
from post.api.serializers import PostSerializer
from post.models import Post
from django.shortcuts import get_object_or_404

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

class PostUpdateApiView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'