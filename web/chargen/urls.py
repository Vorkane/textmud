from django.urls import path
from web.chargen import views

urlpatterns = [
    # url: /chargen/
    path("", views.index, name='chargen-index'),
    # url: /chargen/5/
    path("<int:app_id>/", views.detail, name="chargen-detail"),
    # url: /chargen/create
    path("create/", views.creating, name='chargen-creating'),
]