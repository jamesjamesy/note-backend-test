from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView

from apps.note.models import Note
from utils.responses import success_response


class DeleteNoteView(APIView):
    """
    حذف یادداشت با فرمت اکشن‌محور
    """

    @extend_schema(
        summary="حذف یادداشت",
        description="حذف یادداشت بر اساس شناسه.",
        responses={200: None},
    )
    def delete(self, request, id):
        if request.user.is_authenticated:
            note = get_object_or_404(Note, id=id, user=request.user)
        else:
            note = get_object_or_404(Note, id=id, user__isnull=True)

        note.delete()

        return success_response(
            data=None,
            message="Note deleted successfully",
            code=status.HTTP_200_OK,
        )
