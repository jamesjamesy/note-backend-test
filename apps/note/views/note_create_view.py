from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView

from apps.note.models import Note
from apps.note.serializers import NoteSerializer, NoteWriteSerializer
from utils.responses import success_response


class CreateNoteView(APIView):
    """
    ایجاد یادداشت جدید با فرمت اکشن‌محور
    """

    @extend_schema(
        summary="ایجاد یادداشت جدید",
        description="یک یادداشت جدید می‌سازد و در صورت احراز هویت، آن را به کاربر متصل می‌کند.",
        request=NoteWriteSerializer,
        responses={201: NoteSerializer},
    )
    def post(self, request):
        serializer = NoteWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # اگر کاربر لاگین کرده باشد، نوت را به نام او ذخیره کن
        if request.user.is_authenticated:
            note = serializer.save(user=request.user)
        else:
            note = serializer.save()

        return success_response(
            data=NoteSerializer(note).data,
            message="Note created successfully",
            code=status.HTTP_201_CREATED,
        )
