from .category_view import ListCategoryView
from .note_create_view import CreateNoteView
from .note_delete_view import DeleteNoteView
from .note_detail_view import DetailNoteView
from .note_list_view import ListNoteView
from .note_update_view import UpdateNoteView
from .register_view import RegisterView

__all__ = [
    "CreateNoteView",
    "ListNoteView",
    "DetailNoteView",
    "UpdateNoteView",
    "DeleteNoteView",
    "ListCategoryView",
    "RegisterView",
]
