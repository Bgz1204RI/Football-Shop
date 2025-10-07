import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from .models import Product
from .forms import ProductForm
from django.contrib import messages

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Account created. Please log in.")
        return redirect("main:login")
    if request.method == "POST" and not form.is_valid():
        messages.error(request, "Registration failed. Please fix the errors.")
    return render(request, "register.html", {"form": form})

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Welcome back, {user.username}!")
        response = HttpResponseRedirect(reverse("main:product_list"))
        response.set_cookie("last_login", str(timezone.now()))
        return response
    if request.method == "POST":
        messages.error(request, "Invalid username or password.")
    return render(request, "login.html", {"form": form})

def logout_user(request):
    logout(request)
    response = redirect("main:login")
    response.delete_cookie("last_login")
    return response

@login_required(login_url="main:login")
def product_list(request):
    # Don't fetch/pass products; JS will load via AJAX.
    context = {"last_login": request.COOKIES.get("last_login", "never")}
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
            messages.success(request, f"Product “{obj.name}” created.")
            return redirect("main:product_list")
        messages.error(request, "Could not create product. Check the form.")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})

@login_required(login_url="main:login")
def product_edit(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"“{product.name}” updated.")
            return redirect("main:product_detail", pk=product.pk)
        messages.error(request, "Update failed. Check the form.")
    else:
        form = ProductForm(instance=product)
    return render(request, "product_form.html", {"form": form, "product": product})

@login_required(login_url="main:login")
def product_delete(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        name = product.name
        product.delete()
        messages.warning(request, f"“{name}” deleted.")
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

# ---- Helpers for AJAX ----
def _pdict(p: Product):
    """Product -> plain dict (JSON-ready), incl. computed fields."""
    return {
        "id": p.id,
        "owner": p.owner.username if p.owner_id else None,
        "name": p.name,
        "price": p.price,
        "description": p.description or "",
        "thumbnail": p.thumbnail or "",
        "category": p.category or "",
        "size": p.size,
        "stock": p.stock,
        "is_featured": p.is_featured,
        "for_sale": p.for_sale,
        "stock_status": p.stock_status(),
        "discount_price": p.discount_status(),
    }

def _json(request):
    """Safe JSON body parser -> dict ({} if empty/bad)."""
    try:
        return json.loads(request.body.decode() or "{}")
    except Exception:
        return {}

# ========== AJAX PRODUCT ENDPOINTS ==========
@login_required(login_url="main:login")
@require_http_methods(["GET"])
def products_list_ajax(request):
    """Return the product list as a slim JSON (uses _pdict)."""
    qs = Product.objects.order_by("-id")
    return JsonResponse({"ok": True, "data": [_pdict(p) for p in qs]})

@login_required(login_url="main:login")
@require_http_methods(["GET"])
def product_get_ajax(request, pk):
    """Return a single product by id (for edit modal)."""
    product = get_object_or_404(Product, pk=pk)
    return JsonResponse({"ok": True, "data": _pdict(product)})

@login_required(login_url="main:login")
@require_http_methods(["POST"])
def product_create_ajax(request):
    d = _json(request)
    try:
        p = Product.objects.create(
            owner=request.user,
            name=str(d.get("name", "")).strip(),
            price=int(d.get("price", 0) or 0),
            description=str(d.get("description", "")).strip(),
            thumbnail=str(d.get("thumbnail", "")).strip(),
            category=str(d.get("category", "")).strip(),
            size=d.get("size", "M"),
            stock=int(d.get("stock", 0) or 0),
            is_featured=bool(d.get("is_featured", False)),
            for_sale=bool(d.get("for_sale", False)),
        )
        messages.success(request, f'Product “{p.name}” created.')
        return JsonResponse({"ok": True, "data": _pdict(p)}, status=201)
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=400)

@login_required(login_url="main:login")
@require_http_methods(["POST", "PATCH"])
def product_update_ajax(request, pk):
    p = get_object_or_404(Product, pk=pk)
    d = _json(request)
    try:
        for fld in ["name", "description", "thumbnail", "category"]:
            if fld in d: setattr(p, fld, str(d[fld]).strip())
        if "price" in d: p.price = int(d["price"])
        if "size" in d: p.size = d["size"]
        if "stock" in d: p.stock = int(d["stock"])
        if "is_featured" in d: p.is_featured = bool(d["is_featured"])
        if "for_sale" in d: p.for_sale = bool(d["for_sale"])
        p.save()
        messages.success(request, f'“{p.name}” updated.')
        return JsonResponse({"ok": True, "data": _pdict(p)})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=400)

@login_required(login_url="main:login")
@require_http_methods(["POST", "DELETE"])
def product_delete_ajax(request, pk):
    p = get_object_or_404(Product, pk=pk)
    name = p.name
    p.delete()
    messages.warning(request, f'“{name}” deleted.')
    return JsonResponse({"ok": True})

@require_http_methods(["POST"])
def ajax_login(request):
    d = _json(request)
    user = authenticate(request,
                        username=str(d.get("username","")).strip(),
                        password=d.get("password",""))
    if not user:
        return JsonResponse({"ok": False, "error": "Invalid credentials"}, status=401)
    login(request, user)
    messages.success(request, f"Welcome back, {user.username}!")
    resp = JsonResponse({"ok": True, "message": "Logged in"})
    resp.set_cookie("last_login", str(timezone.now()))
    return resp

@require_http_methods(["POST"])
def ajax_register(request):
    d = _json(request)
    username = str(d.get("username","")).strip()
    password = d.get("password","")
    if not username or not password:
        return JsonResponse({"ok": False, "error": "Username & password required"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"ok": False, "error": "Username already taken"}, status=400)
    try:
        validate_password(password)
    except ValidationError as ve:
        return JsonResponse({"ok": False, "error": "; ".join(ve.messages)}, status=400)
    User.objects.create_user(username=username, password=password)
    messages.success(request, "Account created. You can log in now.")
    return JsonResponse({"ok": True, "message": "Registered"})

@require_http_methods(["POST"])
def ajax_logout(request):
    logout(request)
    messages.success(request, "Logged out.")
    resp = JsonResponse({"ok": True, "message": "Logged out"})
    resp.delete_cookie("last_login")
    return resp
# ============================================


def about(request):
    context = {
        "app_name": "Football Shop",
        "student_name": "Bagas Zharif",
        "student_class": "PBP KKI",
    }
    return render(request, "about.html", context)