from django import forms
from .models import Content
class ContentForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Content.objects.filter(parent__isnull=True), required=False)

    class Meta:
        model = Content
        fields = ['title', 'parent']

    def save(self, commit=True):
        instance = super().save(commit=False)
        parent = self.cleaned_data.get('parent')
        if parent:
            instance.parent = parent
        else:
            instance.parent = None  # Установка parent на None, если ничего не выбрано
        if commit:
            instance.save()
        return instance


from django import forms
from .models import ContentChild

class ContentChildForm(forms.ModelForm):
    class Meta:
        model = ContentChild
        fields = ['title', 'body', 'parent']
        widgets = {
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }
