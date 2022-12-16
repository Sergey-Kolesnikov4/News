from django import forms
from django.core.exceptions import ValidationError
from .models import News


class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=34)
    class Meta:
        model = News
        fields = ['title','text','category','author']

        def clean(self):
            cleaned_data = super().clean()
            title = cleaned_data.get('title')
            text = cleaned_data.get('text')

            if title == text:
                raise ValidationError('Текст не должен быть идентичен заголовку')
            return cleaned_data


class ArticleForm(forms.ModelForm):
    title = forms.CharField(max_length=34)
    class Meta:
        model = News
        fields = ['title','text','category','author']

        def clean(self):
            cleaned_data = super().clean()
            title = cleaned_data.get('title')
            text = cleaned_data.get('text')

            if title == text:
                raise ValidationError('Текст не должен быть идентичен заголовку')
            return cleaned_data
