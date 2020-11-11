from django import forms
from .models import Diary

class DiaryCreateForm(forms.ModelForm):

    class Meta:
        model = Diary
        fields = ('content', 'photo1', 'photo2', 'photo3',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
