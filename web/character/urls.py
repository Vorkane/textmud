from django.urls import path
from web.character.views import sheet

urlpatterns = [
    path("sheet/<int:object_id>", sheet, name="sheet")
]