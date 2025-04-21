from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users.views import UserDetailView, IsAuthenticatedView, UserListView

urlpatterns = [
    path('token/', obtain_auth_token, name='token-auth'),  # Token generation endpoint
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('users/', UserListView.as_view(), name='user-detail'),
    path('is_authenticated/', IsAuthenticatedView.as_view(), name='user-authenticated'),
]
