from django import forms
from . import models


class OrderedProductFEForm(forms.ModelForm):

    class Meta:
        model = models.OrderedProduct
        fields = "__all__"

        widgets = {
            "order": forms.HiddenInput(),
            "product": forms.HiddenInput(),
            "size": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "min": "1"})
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields["size"].queryset = self.instance.product.sizes.all()
        except:
            pass



class OrderedProductAdminForm(forms.ModelForm):

    class Meta:
        model = models.OrderedProduct
        fields = "__all__"




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields["size"].queryset = self.instance.product.sizes.all()
        except:
            pass

        