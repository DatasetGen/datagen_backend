from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import CustomUserSerializer  # Assuming you have a user serializer

User = get_user_model()

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })


class IsAuthenticatedView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users to check auth status

    def get(self, request):
        if request.user.is_authenticated:
            return Response({"authenticated": True})
        return Response({"authenticated": False})


class UserListView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can see the list

    def get(self, request):
        users = User.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
