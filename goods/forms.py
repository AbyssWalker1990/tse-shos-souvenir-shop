from django.forms import ModelForm
from .models import Category, Product


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'featured_img', ]
        labels = {
            'name': 'Назва категорії',
            'featured_img': 'Зображення',
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['prod_category', 'name', 'description', 'price', 'discount',
                  'featured_img', 'img1', 'img2', 'img3']
        labels = {
            'prod_category': 'Категорія',
            'name': 'Назва товару',
            'description': 'Опис товару',
            'price': 'Ціна',
            'discount': 'Знижка',
            'featured_img': 'Основне зображення',
            'img1': 'Слайдер 1',
            'img2': 'Слайдер 2',
            'img3': 'Слайдер 3',
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['description'].required = False
        self.fields['price'].required = False
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

