from django.forms import ModelForm
from .models import *
"""
class RoundGroupForm(ModelForm):
    class Meta:
        model = RoundGroup
        fields = ['name', 'rounds']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (instance:=kwargs.get('instance')):
            rounds = Round.objects.filter(event__tournament=instance.tournament).order_by('name')
        else:
            rounds = []
        w = self.fields['rounds'].widget
        choices = []
        for round in rounds:
            choices.append((round.id, f'{round.event.code} {round.get_name_display()}'))
        w.choices = choices
        w.attrs['style'] = 'width: 200px;'
        if choices:
            w.attrs['size'] = min(10, len(choices))
"""