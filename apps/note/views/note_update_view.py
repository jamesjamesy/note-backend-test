from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from apps.note.models import Note
from apps.note.serializers import NoteSerializer, NoteWriteSerializer
from utils.responses import success_response


class UpdateNoteView(APIView):
    """
    ویرایش یادداشت با فرمت اکشن‌محور (پشتیبانی از PUT و PATCH)
    """

    @extend_schema(
        summary="ویرایش یادداشت",
        description="ویرایش کامل عنوان، محتوا یا دسته‌بندی یادداشت.",
        request=NoteWriteSerializer,
        responses={200: NoteSerializer},
    )
    def put(self, request, id):
        return self._update(request, id, partial=False)

    @extend_schema(
        summary="ویرایش جزئی یادداشت",
        description="ویرایش بخشی از اطلاعات یادداشت.",
        request=NoteWriteSerializer,
        responses={200: NoteSerializer},
    )
    def patch(self, request, id):
        return self._update(request, id, partial=True)

    def _update(self, request, id, partial=False):
        if request.user.is_authenticated:
            note = get_object_or_404(Note, id=id, user=request.user)
        else:
            note = get_object_or_404(Note, id=id, user__isnull=True)

        serializer = NoteWriteSerializer(note, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_note = serializer.save()

        return success_response(
            data=NoteSerializer(updated_note).data,
            message="Note updated successfully",
        )
