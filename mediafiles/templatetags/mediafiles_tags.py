from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

from django.template import Library, Node, TemplateSyntaxError, Variable
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from mediafiles.settings import MEDIAFILES_IMAGES, MEDIAFILES_PYGMENTS_STYLE


register = Library()

class FileContentNode(Node):
    def __init__(self, path, context_var=None):
        self.context_var = context_var
        self.path = Variable(path)

    def render(self, context):
        path = self.path.resolve(context)
        content_type = path.content_type

        if content_type in MEDIAFILES_IMAGES:
            rendered = render_to_string('mediafiles/wrapper/image.html',
                                        context)
        else:
            try:
                lexer = get_lexer_for_filename(path.name,
                                               stripnl=False,
                                               tabsize=4)
            except ClassNotFound:
                rendered = None
            else:
                formatter = HtmlFormatter(linenos='inline',
                                          lineanchors='l',
                                          nobackground=True,
                                          style=MEDIAFILES_PYGMENTS_STYLE)
                rendered = mark_safe(highlight(path.content, lexer, formatter))

        if self.context_var is not None:
            context[self.context_var] = rendered
            return u''

        return rendered

def do_get_gile_content(parser, token):
    try:
        tagname, path, unused, context_var = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, \
              'Usage: {% get_file_content PATH as CONTEXT_VAR %}'
    return FileContentNode(path, context_var)
register.tag('get_file_content', do_get_gile_content)

def do_show_file_content(parser, token):
    try:
        tagname, path = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, \
              'Usage: {% show_file_content PATH %}'
    return FileContentNode(path)
register.tag('show_file_content', do_show_file_content)
