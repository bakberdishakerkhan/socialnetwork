from django import forms
from .models import News

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
       kwargs.setdefault('widget', MultipleFileInput)
       kwargs.setdefault('required', False)
       super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean 
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
       


class PostForm(forms.ModelForm):
    images = MultipleFileField()
    class Meta:
        model = News
        fields = ('title', 'content', 'images')

    

    