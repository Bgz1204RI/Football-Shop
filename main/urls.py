# main/urls.py
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/create/", views.product_create, name="product_create"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("product/<int:id>/edit/", views.product_edit, name="product_edit"),
    path("product/<int:id>/delete/", views.product_delete, name="product_delete"),

    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),

    path("xml/", views.show_xml, name="show_xml"),
    path("json/", views.show_json, name="show_json"),
    path("xml/<int:id>/", views.show_xml_by_id, name="show_xml_by_id"),
    path("json/<int:id>/", views.show_json_by_id, name="show_json_by_id"),
    path("about/", views.about, name="about"),

]
