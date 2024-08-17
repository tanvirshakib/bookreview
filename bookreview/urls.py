from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reviews.views import UserViewSet, BookViewSet, ReviewViewSet, register, user_login, user_logout
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviews.urls')),
    path('api/', include(router.urls)),
    path('api/register/', register, name='register'),
    path('api/login/', user_login, name='login'),
    path('api/logout/', user_logout, name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

