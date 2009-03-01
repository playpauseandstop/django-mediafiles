import string

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.util import ClassNotFound

from django.template import Library, Node, TemplateSyntaxError, Variable
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from mediafiles.settings import MEDIAFILES_IMAGES, MEDIAFILES_PYGMENTS_STYLE


register = Library()

class FileContentNode(Node):
    def __init__(self, path, content=None, content_editable=None):
        self.content, self.content_editable = content, content_editable
        self.path = Variable(path)

    def render(self, context):
        path = self.path.resolve(context)
        content_editable = False
        content_type = path.content_type

        if content_type in MEDIAFILES_IMAGES:
            rendered = render_to_string('mediafiles/wrapper/image.html',
                                        context)
        else:
            lexer = None
            lexer_options = {'stripnl': False,
                             'tabsize': 4}

            try:
                lexer = guess_lexer_for_filename(path.name,
                                                 path.content,
                                                 **lexer_options)
            except ClassNotFound:
                if not path.extension and not path.is_executable():
                    lexer = get_lexer_by_name('text',
                                              **lexer_options)

            if lexer is not None:
                formatter = HtmlFormatter(linenos='inline',
                                          lineanchors='l',
                                          nobackground=True,
                                          style=MEDIAFILES_PYGMENTS_STYLE)
                rendered = mark_safe(highlight(path.content, lexer, formatter))
                content_editable = path.is_writeable()
            else:
                rendered = None

        if self.content is not None:
            context[self.content] = rendered
            context[self.content_editable] = content_editable
            return u''

        return rendered

def do_get_gile_content(parser, token):
    try:
        tagname, path, unused, context_vars = token.split_contents()
        content, content_editable = map(string.strip, context_vars.split(','))
    except ValueError:
        raise TemplateSyntaxError, \
              'Usage: {% get_file_content PATH as CONTEXT_VAR,CONTEXT_VAR %}'
    return FileContentNode(path, content, content_editable)
register.tag('get_file_content', do_get_gile_content)

def do_show_file_content(parser, token):
    try:
        tagname, path = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, \
              'Usage: {% show_file_content PATH %}'
    return FileContentNode(path)
register.tag('show_file_content', do_show_file_content)
