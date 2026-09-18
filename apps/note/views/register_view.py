from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from apps.note.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    ثبت‌نام کاربر جدید
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": user.username,
                "message": "کاربر با موفقیت ثبت شد",
            },
            status=status.HTTP_201_CREATED,
        )
