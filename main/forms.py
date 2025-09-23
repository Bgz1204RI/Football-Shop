from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name", "price", "description", "thumbnail", "category",
            "size", "stock", "is_featured", "for_sale"
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_price(self):
        p = self.cleaned_data["price"]
        if p < 0:
            raise forms.ValidationError("Price must be ≥ 0.")
        return p

    def clean_stock(self):
        s = self.cleaned_data["stock"]
        if s < 0:
            raise forms.ValidationError("Stock must be ≥ 0.")
        return s
