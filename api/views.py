from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import Product, User
from .serializers import ProductSerializer, UserSerializer, UserLoginSerializer
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from datetime import datetime


# User View
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        username = request.data.get('username')

        if username:
            instance.username = username
            instance.save()

            return Response({'message': 'Username updated successfully.'})
        else:
            return Response({'message': 'No username provided.'}, status=400)
    

# User login
class UserLoginView(viewsets.ModelViewSet):
    serializer_class = UserLoginSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = password=serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'success': 'User logged in successfully'})
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        

# User logout
class UserLogoutView(viewsets.ModelViewSet):
    def logout(self, request, *args, **kwargs):
        logout(request)
        return Response({'success': 'User logged out successfully'})
    

# product view
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # creation
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # update
    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.user != self.request.user:
            raise PermissionDenied("You don't have permission to update this product.")
        else:
            serializer.save()
        
        # active inactive after 2 month
        two_months_ago = timezone.now() - timezone.timedelta(days=60)
        print(two_months_ago)
        print(instance.created_at)

        # if instance.created_at > two_months_ago:
        #     serializer.validated_data['is_active'] = False
        # else:
        #     serializer.validated_data['is_active'] = True
        # serializer.save()

    # delete
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You don't have permission to delete this product.")

        else:
            instance.delete()

















        # if instance.is_inactive():
        #     serializer.validated_data['active'] = False
        # serializer.save()

    # def perform_update(self, serializer):
    #     product = serializer.instance
    #     print
    #     if not product.is_registered_before_2_month():
    #         serializer.save(user=self.request.user)
    #     else:
    #         product.is_active = False
    #         product.save()
    #         return Response({'details':'Product maded to inactive ',}, status=status.HTTP_200_ok)

# class ProductViewSet(viewsets.ModelViewSet):
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer

    # def perform_update(self, serializer):
    #     instance = serializer.instance
    #     if instance.is_inactive():
    #         serializer.validated_data['active'] = False
    #     serializer.save()


