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
        return redirect("login")
    return render(request, "register.html", {"form": form})

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("product_list"))
        response.set_cookie("last_login", str(timezone.now()))
        return response
    return render(request, "login.html", {"form": form})

def logout_user(request):
    logout(request)
    response = redirect("login")
    response.delete_cookie("last_login")
    return response

@login_required(login_url="login")
def product_list(request):
    product = Product.objects.filter(owner=request.user).order_by("-id")
    context = {
        "product": product,
        "last_login": request.COOKIES.get("last_login", "never"),
    }
    return render(request, "product_list.html", context)

@login_required(login_url="login")
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    return render(request, "product_detail.html", {"product": product})

@login_required(login_url="login")
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})

@login_required(login_url="login")
def show_xml(request):
    data = Product.objects.filter(owner=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required(login_url="login")
def show_json(request):
    data = Product.objects.filter(owner=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url="login")
def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id, owner=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required(login_url="login")
def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id, owner=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def about(request):
    context = {
        "app_name": "Football Shop",
        "student_name": "Bagas Zharif",
        "student_class": "PBP KKI",
    }
    return render(request, "about.html", context)
