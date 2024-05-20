from django import forms
from .models import Content
from django import forms
from .models import Content


from django import forms
from .models import Content

class ContentForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Content.objects.filter(parent__isnull=True), required=False)
    image1 = forms.ImageField(required=False)
    image2 = forms.ImageField(required=False)
    image3 = forms.ImageField(required=False)

    class Meta:
        model = Content
        fields = ['title', 'parent', 'image1', 'image2', 'image3']

    def save(self, commit=True):
        instance = super().save(commit=False)
        parent = self.cleaned_data.get('parent')
        instance.parent = parent if parent else None

        if commit:
            instance.save()
            self._save_m2m()
            self._save_images(instance)

        return instance

    def _save_images(self, instance):
        # Handle image fields and save them to the instance
        for i in range(1, 4):
            image_field = f'image{i}'
            image = self.cleaned_data.get(image_field)
            if image:
                setattr(instance, image_field, image)
        instance.save()


from django import forms
from .models import ContentChild

class ContentChildForm(forms.ModelForm):
    class Meta:
        model = ContentChild
        fields = ['title', 'body', 'parent']
        widgets = {
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    is_superuser = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_superuser')

