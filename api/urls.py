from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductActiveView, ProductViewSet, UserLoginView, UserViewSet, UserLogoutView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', UserLoginView.as_view({'post': 'create'}), name='login'),
    path('api/logout/', UserLogoutView.as_view({'get': 'logout'}), name='logout'),
    path('api/activate/<int:pk>/', ProductActiveView.as_view({'put': 'activate'}), name='activate'),

]