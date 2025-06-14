from django import forms
from .models import Product

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
    'бесплатно', 'обман', 'полиция', 'радар'
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'purchase_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })
        # Отдельно для FileInput (картинки)
        if 'image' in self.fields:
            self.fields['image'].widget.attrs.update({
                'class': 'form-control form-control-file'
            })

    def _check_forbidden(self, text, field):
        for word in FORBIDDEN_WORDS:
            if word in text.lower():
                raise forms.ValidationError(f'Поле "{field}" содержит запрещённое слово: "{word}"')

    def clean_name(self):
        value = self.cleaned_data.get('name', '')
        self._check_forbidden(value, 'Наименование')
        return value

    def clean_description(self):
        value = self.cleaned_data.get('description', '')
        self._check_forbidden(value, 'Описание')
        return value

    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price
