from django import forms
from django.utils.translation import ugettext as _

__all__ = ('ChmodPathForm', 'ChownPathForm', 'MakeDirectoryForm',
           'RenamePathForm')

class ChmodPathForm(forms.Form):
    pass

class ChownPathForm(forms.Form):
    pass

class MakeDirectoryForm(forms.Form):
    name = forms.CharField(label=_('Directory name'), min_length=1,
                           max_length=64)

    def __init__(self, *args, **kwargs):
        if not 'path' in kwargs:
            raise TypeError, 'Required keyword arg "path" was not supplied.'
        self.path = kwargs.pop('path')
        super(MakeDirectoryForm, self).__init__(*args, **kwargs)

class RenamePathForm(forms.Form):
    pass
