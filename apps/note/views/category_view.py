from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from apps.note.models import Category
from apps.note.serializers import CategorySerializer
from utils.responses import success_response


class ListCategoryView(APIView):
    """
    دریافت لیست دسته‌بندی‌ها با فرمت اکشن‌محور
    """

    @extend_schema(
        summary="لیست دسته‌بندی‌ها",
        description="دریافت تمامی دسته‌بندی‌های عمومی یادداشت‌ها.",
        responses={200: CategorySerializer(many=True)},
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return success_response(
            data=serializer.data,
            message="Categories retrieved successfully",
        )
