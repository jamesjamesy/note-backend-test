from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from apps.note.models import Note
from apps.note.serializers import NoteSerializer
from utils.responses import success_response


class DetailNoteView(APIView):
    """
    نمایش جزئیات یک یادداشت با فرمت اکشن‌محور
    """

    @extend_schema(
        summary="جزئیات یادداشت",
        description="دریافت اطلاعات کامل یک یادداشت بر اساس شناسه.",
        responses={200: NoteSerializer},
    )
    def get(self, request, id):
        if request.user.is_authenticated:
            note = get_object_or_404(Note, id=id, user=request.user)
        else:
            note = get_object_or_404(Note, id=id, user__isnull=True)

        return success_response(
            data=NoteSerializer(note).data,
            message="Note retrieved successfully",
        )
