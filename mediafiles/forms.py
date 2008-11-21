from django import forms
from django.conf import settings
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

    def clean_name(self):
        name = self.cleaned_data['name']
        dirs = self.path.list_dir(filter='dirs')

        for dir in dirs:
            if dir.name == name:
                raise forms.ValidationError, \
                      _('Directory with name "%s" exists on this path.' % \
                        name)

        return name

    def save(self):
        return self.path.mkdir(self.cleaned_data['name'])

class RenamePathForm(forms.Form):
    oldname = forms.CharField(label=_('Old name'), min_length=1, max_length=64,
        widget=forms.TextInput(attrs={'class': 'disabled',
                                      'disabled': 'disabled'}))
    newname = forms.CharField(label=_('New name'), min_length=1, max_length=64)

    def __init__(self, *args, **kwargs):
        if not 'path' in kwargs:
            raise TypeError, 'Required keyword arg "path" was not supplied.'
        self.path = kwargs.pop('path')
        super(RenamePathForm, self).__init__(*args, **kwargs)

    def clean_newname(self):
        newname = self.cleaned_data['newname']
        items = self.path.parent.list_dir()

        for item in items:
            if item.name == newname:
                raise forms.ValidationError, \
                      _('Can not rename "%s" to "%s", cause this path ' \
                        'existsed here.' % (self.path.name, newname))

        return newname

    def save(self):
        return self.path.rename(self.cleaned_data['newname'])
