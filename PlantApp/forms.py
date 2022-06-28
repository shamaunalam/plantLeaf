from django.forms import ModelForm
from .models import Query,Answer

class QueryForm(ModelForm):
    class Meta:
        model = Query
        fields=['query','image']

