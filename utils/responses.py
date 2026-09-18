from rest_framework import status
from rest_framework.response import Response


def success_response(data=None, message="Operation successful", code=status.HTTP_200_OK):
    """
    تابع کمکی تولید پاسخ استاندارد موفق:
    {
        "meta": {
            "message": message,
            "errors": {}
        },
        "data": data
    }
    """
    return Response(
        {
            "meta": {
                "message": message,
                "errors": {},
            },
            "data": data,
        },
        status=code,
    )


def error_response(message="Operation failed", errors=None, code=status.HTTP_400_BAD_REQUEST):
    """
    تابع کمکی تولید پاسخ استاندارد خطا:
    {
        "meta": {
            "message": message,
            "errors": errors or {}
        },
        "data": None
    }
    """
    return Response(
        {
            "meta": {
                "message": message,
                "errors": errors or {},
            },
            "data": None,
        },
        status=code,
    )
