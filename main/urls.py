# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/add/", views.product_create, name="product_add"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),

    path("xml/", views.show_xml, name="show_xml"),
    path("json/", views.show_json, name="show_json"),
    path("xml/<int:id>/", views.show_xml_by_id, name="show_xml_by_id"),
    path("json/<int:id>/", views.show_json_by_id, name="show_json_by_id"),
]
