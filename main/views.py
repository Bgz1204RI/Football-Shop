from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from .models import Product
from .forms import ProductForm

def product_list(request):
    products = Product.objects.all().order_by("-id")
    return render(request, "product_list")

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})

def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})

#Data delivery (XML/JSON)
def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id) 
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def about(request):
    context = {
        "app_name": "Football Shop",     # your app’s name
        "student_name": "Bagas Zharif",  # replace with your real name
        "student_class": "CS 2024"       # replace with your class
    }
    return render(request, "about.html", context)
