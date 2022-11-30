from django.forms import ModelForm
from .models import Category


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
