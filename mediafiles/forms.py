import os

from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _

from settings import *


__all__ = ('EditFileForm', 'MakeDirectoryForm', 'MakeFileForm',
           'RemovePathForm', 'RenamePathForm', 'UploadForm')

class EditFileForm(forms.Form):
    content = forms.CharField(label=_('Content'), required=False,
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 25}))

    def __init__(self, *args, **kwargs):
        if not 'path' in kwargs:
            raise TypeError, 'Required keyword arg "path" was not supplied.'
        self.path = kwargs.pop('path')

        kwargs.update({'initial': {'content': self.path.content}})
        super(EditFileForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data
        content = cd.get('content', '')

        try:
            self.path.write(content)
        except Exception, e:
            e = forms.ValidationError(
                _("Couldn't write to file at this path cause system error.")
            )
            self._errors['content'] = e.messages
            raise e

        return cd

class MakeDirectoryForm(forms.Form):
    name = forms.CharField(label=_('Directory name'), max_length=64)

    def __init__(self, *args, **kwargs):
        if not 'path' in kwargs:
            raise TypeError, 'Required keyword arg "path" was not supplied.'
        self.path = kwargs.pop('path')
        super(MakeDirectoryForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if name in MEDIAFILES_DIRS_BLACKLIST:
            raise forms.ValidationError, \
                  _('Directory\'s name "%s" blacklisted by server settings.' % \
                    name)

        dirs = self.path.list_dir(filter='dirs')
        for dir in dirs:
            if dir.name == name:
                raise forms.ValidationError, \
                      _('Directory with name "%s" exists on this path.' % \
                        name)

        return name

    def clean(self):
        cd = self.cleaned_data

        if not cd:
            return cd

        try:
            self.path.mkdir(self.cleaned_data['name'])
        except Exception, e:
            e = forms.ValidationError(
                _("Couldn't make directory at this path cause system error.")
            )
            self._errors['name'] = e.messages
            raise e

        return cd

class MakeFileForm(forms.Form):
    name = forms.CharField(label=_('File name'), max_length=64)
    content = forms.CharField(label=_('Content'), required=False,
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 15}))

    def __init__(self, *args, **kwargs):
        if not 'path' in kwargs:
            raise TypeError, 'Required keyword arg "path" was not supplied.'
        self.path = kwargs.pop('path')
        super(MakeFileForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']

        if name in MEDIAFILES_FILES_BLACKLIST:
            raise forms.ValidationError, \
                  _('File\'s name "%s" blacklisted by server settings.' %
                    name)

        ext = os.path.splitext(name)[1]
        if ext in MEDIAFILES_EXTS_BLACKLIST:
            raise forms.ValidationError, \
                  _('File\'s extension "%s" blacklisted by server settings.' % \
                    ext)

        files = self.path.list_dir(filter='files')
        for f in files:
            if f.name == name:
                raise forms.ValidationError, \
                      _('File with name "%s" existed on this path.' % f.name)

        return name

    def clean(self):
        cd = self.cleaned_data

        if not cd or not 'name' in cd:
            return cd

        try:
            self.path.mkfile(cd['name'], cd['content'])
        except Exception, e:
            print type(e), e
            e = forms.ValidationError(
                _("Couldn't make new file cause server error.")
            )
            self._errors['name'] = e.messages
            raise e

        return cd

class RemovePathForm(forms.Form):
    accept_remove = forms.BooleanField(label=_('Accept remove'), required=True)

    def __init__(self, *args, **kwargs):
        if not 'path' in kwargs:
            raise TypeError, 'Required keyword arg "path" was not supplied.'
        self.path = kwargs.pop('path')
        super(RemovePathForm, self).__init__(*args, **kwargs)

        if self.path.is_dir():
            self.fields['accept_remove'].help_text = \
                _('All items existed in directory will be deleted.')

    def clean(self):
        cd = self.cleaned_data

        if not cd:
            return cd

        try:
            self.path.remove()
        except Exception, e:
            type = self.path.is_dir() and _('directory') or _('file')
            e = forms.ValidationError(
                _("Couldn't remove %s cause system error." % type)
            )
            self._errors['accept_remove'] = e.messages
            raise e

        return cd

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
                      _('Couldn\'t rename "%s" to "%s", cause this path ' \
                        'existed here.' % (self.path.name, newname))

        return newname

    def clean(self):
        cd = self.cleaned_data

        if not cd or not 'newname' in cd:
            return cd

        try:
            self.path.rename(self.cleaned_data['newname'])
        except Exception, e:
            type = self.path.is_dir() and _('directory') or _('file')
            e = forms.ValidationError(
                _("Couldn't rename %s cause system error." % unicode(type))
            )
            self._errors['newname'] = e.messages
            raise e

        return cd

class UploadForm(forms.Form):
    file = forms.FileField(label=_('Select file to upload'), required=True)
    accept_rewrite = forms.BooleanField(label=_('Accept file rewrite'),
        required=False)

    def __init__(self, *args, **kwargs):
        if not 'path' in kwargs:
            raise TypeError, 'Required keyword arg "path" was not supplied.'
        self.path = kwargs.pop('path')
        super(UploadForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        file = self.cleaned_data['file']

        if file.name in MEDIAFILES_FILES_BLACKLIST:
            raise forms.ValidationError, \
                  _('File\'s name "%s" blacklisted by server settings.' %
                    file.name)

        ext = os.path.splitext(file.name)[1]
        if ext in MEDIAFILES_EXTS_BLACKLIST:
            raise forms.ValidationError, \
                  _('File\'s extension "%s" blacklisted by server settings.' % \
                    ext)

        files = self.path.list_dir(filter='files')
        for f in files:
            if f.name == file.name:
                setattr(self, '__file_existed', f.name)
                break

        return file

    def clean_accept_rewrite(self):
        accept_rewrite = self.cleaned_data['accept_rewrite']

        if hasattr(self, '__file_existed') and not accept_rewrite:
            name = getattr(self, '__file_existed')
            raise forms.ValidationError, \
                  _('File with name "%s" existed on this path.' % name)

        return accept_rewrite

    def clean(self):
        cd = self.cleaned_data

        if not cd or not 'file' in cd:
            return cd

        try:
            self.path.upload(cd['file'])
        except Exception, e:
            e = forms.ValidationError(
                _('Couldn\'t upload file cause system error.')
            )
            self._errors['file'] = e.messages
            raise e

        return cd
