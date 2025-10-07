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

    path("ajax/products/", views.products_list_ajax, name="products_list_ajax"),
    path("ajax/product/<int:pk>/", views.product_get_ajax, name="product_get_ajax"),
    path("ajax/product/create/", views.product_create_ajax, name="product_create_ajax"),
    path("ajax/product/<int:pk>/update/", views.product_update_ajax, name="product_update_ajax"),
    path("ajax/product/<int:pk>/delete/", views.product_delete_ajax, name="product_delete_ajax"),

    # AJAX auth <remember>
    path("ajax/auth/login/", views.ajax_login, name="api_login"),
    path("ajax/auth/register/", views.ajax_register, name="api_register"),
    path("ajax/auth/logout/", views.ajax_logout, name="api_logout"),
]
