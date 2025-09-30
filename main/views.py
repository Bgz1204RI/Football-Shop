from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from .models import Product
from .forms import ProductForm

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("main:login")
    return render(request, "register.html", {"form": form})

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:product_list"))
        response.set_cookie("last_login", str(timezone.now()))
        return response
    return render(request, "login.html", {"form": form})

def logout_user(request):
    logout(request)
    response = redirect("main:login")
    response.delete_cookie("last_login")
    return response

@login_required(login_url="main:login")
def product_list(request):
    products = Product.objects.all().order_by("-id")  
    context = {
        "product": products,
        "last_login": request.COOKIES.get("last_login", "never"),
    }
    return render(request, "product_list.html", context)

@login_required(login_url="main:login")
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  
    return render(request, "product_detail.html", {"product": product})

@login_required(login_url="main:login")
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect("main:product_list")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})

@login_required(login_url="main:login")
def product_edit(request, id):
    product = get_object_or_404(Product, pk=id)  # no owner check
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("main:product_detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "product_form.html", {"form": form, "product": product})

@login_required(login_url="main:login")
def product_delete(request, id):
    product = get_object_or_404(Product, pk=id)  
    if request.method == "POST":
        product.delete()
        return redirect("main:product_list")
    return render(request, "product_confirm_delete.html", {"product": product})

# XML/JSON endpoints: expose all
@login_required(login_url="main:login")
def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required(login_url="main:login")
def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url="main:login")
def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required(login_url="main:login")
def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def about(request):
    context = {
        "app_name": "Football Shop",
        "student_name": "Bagas Zharif",
        "student_class": "PBP KKI",
    }
    return render(request, "about.html", context)