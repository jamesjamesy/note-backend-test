from django.urls import path

from .views import (
    CreateNoteView,
    DeleteNoteView,
    DetailNoteView,
    ListNoteView,
    UpdateNoteView,
)

app_name = "note"

urlpatterns = [
    # CRUD Note Endpoints
    path("create", CreateNoteView.as_view(), name="create-note"),
    path("list", ListNoteView.as_view(), name="list-note"),
    path("detail/<int:id>", DetailNoteView.as_view(), name="detail-note"),
    path("update/<int:id>", UpdateNoteView.as_view(), name="update-note"),
    path("delete/<int:id>", DeleteNoteView.as_view(), name="delete-note"),
]