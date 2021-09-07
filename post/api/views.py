from django.http import HttpResponse, JsonResponse
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ( ListAPIView,
                                      RetrieveAPIView,
                                      DestroyAPIView,
                                      UpdateAPIView,
                                      CreateAPIView,
                                      RetrieveUpdateAPIView,
                                    )

from rest_framework.mixins import CreateModelMixin,ListModelMixin,DestroyModelMixin

from account.api.throttles import RegisterThrottle
from post.api.paginations import PostPagination
from post.api.permisions import IsOwner
from post.api.serializers import PostSerializer,PostCreateUpdateSerializer
from post.models import Post
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,IsAdminUser)
class PostListApiView(ListAPIView):
    throttle_scope = 'plist'

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields=['title','content']
    # throttle_classes = [RegisterThrottle]
    pagination_class = PostPagination
    def get_queryset(self):
        queryset=Post.objects.filter(draft=False)
        return queryset

    '''combine create and list using CreateModelMixin'''
    # def post(self,request,*args,**kwargs):
    #     return self.create(request,*args,**kwargs)
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

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

# class PostDeleteApiView(DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     lookup_field = 'slug'
#     permission_classes = [IsOwner]

class PostUpdateApiView(RetrieveUpdateAPIView,DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]
    '''combine delete and list using DestroyModelMixin'''
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

class PostCreateApiView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    '''combine create and list using ListModelMixin'''
    # def get(self,request,*args,**kwargs):
    #     print(args)
    #     print(kwargs)
    #     return self.list(self, request, *args, **kwargs)



