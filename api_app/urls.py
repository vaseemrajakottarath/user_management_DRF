from django.urls import path
from django.conf.urls import include
from.views import RegisterView, UserDetails, UsersList
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

   path('register/',RegisterView.as_view(),name='register'),
   
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('UsersList/',UsersList.as_view(),name='UsersList'),
   path('UserDetails/<int:pk>/',UserDetails.as_view(),name='UserDetails'),
]