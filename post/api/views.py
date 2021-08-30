from rest_framework.generics import ListAPIView

from post.models import Post


class PostListApiView(ListAPIView):
    queryset = Post.objects.all()
