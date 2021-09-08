from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView,get_object_or_404,CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import NotAuthenticated
from account.api.serializers import UserSerializer, ChangePasswordSerializer, RegisterUserSerializer
from .throttles import RegisterThrottle

class ProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        queryset=self.get_queryset()
        obj=get_object_or_404(queryset,id=self.request.user.id)
        return obj

class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated,]
    def get_object(self):
        return self.request.user

    def put(self,request,*args,**kwargs):
        self.object=self.get_object()
        serializer=ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password=serializer.data.get('old_password')
            if not self.object.check_password(old_password):
                return Response({'old_password':'wrong_password'},status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            update_session_auth_hash(self.request,self.object)
            return Response('successfully',status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(CreateAPIView):
    model = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [NotAuthenticated,]
    throttle_classes = [RegisterThrottle]
