from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from apps.note.models import Note
from apps.note.serializers import NoteSerializer
from utils.responses import success_response


class ListNoteView(APIView):
    """
    دریافت لیست یادداشت‌ها به صورت صفحه‌بندی‌شده
    """
    pagination_class = PageNumberPagination

    @extend_schema(
        summary="لیست یادداشت‌ها",
        description="دریافت لیست یادداشت‌های کاربر یا یادداشت‌های عمومی به صورت صفحه‌بندی‌شده.",
        responses={200: NoteSerializer(many=True)},
    )
    def get(self, request):
        if request.user.is_authenticated:
            queryset = Note.objects.filter(user=request.user)
        else:
            queryset = Note.objects.filter(user__isnull=True)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = NoteSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = NoteSerializer(queryset, many=True)
        return success_response(
            data={"count": queryset.count(), "results": serializer.data},
            message="Retrieved successfully",
        )
