from docutils import nodes
from docutils.utils import unescape
from docutils.parsers.rst import Directive, directives
from sphinx.util.nodes import split_explicit_title, set_source_info

# Cross reference with document and label
# Syntax: :docref`Title <rawdocname:label>`
# Backends: html, man, others
# - title is mandatory, for manual page backend will append "in rawdocname" if it's in another document
# - label is not yet validated, can be duplicate in more documents
# - rawdocname is without extension
def role_docref(name, rawtext, text, lineno, inliner, options={}, content=[]):
    env = inliner.document.settings.env
    text = unescape(text)
    has_explicit_title, title, target = split_explicit_title(text)
    if not has_explicit_title:
        msg = inliner.reporter.error(f"docref requires title: {rawtext}", line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    try:
        docname, label = target.split(':', 1)
    except ValueError:
        msg = inliner.reporter.error(f"invalid docref syntax {target}", line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    # inliner.reporter.warning(f"DBG: docname={docname} label={label} env.docname={env.docname} title={title}")

    # Validate doc
    if docname not in env.found_docs:
        docs = list(env.found_docs)
        msg = inliner.reporter.error(f"document not found {docname} (%s" % (docs), line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    # TODO: validate label

    suffix = ''
    if env.app.builder.name == 'html':
        suffix = '.html'
    elif env.app.builder.name == 'man':
        suffix = '//'

    titlesuffix = ''
    if docname != env.docname:
        titlesuffix = f" (in {docname})"

    try:
        ref_node = nodes.reference(rawtext, title + titlesuffix,
                                   refuri=f"{docname}{suffix}#{label}", **options)
    except ValueError:
        msg = inliner.reporter.error('invalid cross reference %r' % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    return [ref_node], []

# Directive to define a label that can appear multiple time (e.g. from an included
# document), no warnings
# Must be used in connection with :docref: to link to the containing rather than
# included document
# Syntax: .. duplabel:: label-name
# Backends: all
class DupLabelDirective(Directive):
    required_arguments = 1

    def run(self):
        label = self.arguments[0]
        target_node = nodes.target('', '', ids=[label])
        env = self.state.document.settings.env
        line_number = self.state.document.current_line
        env.domaindata['std']['labels'][label] = (env.docname, label, line_number)
        set_source_info(self, target_node)
        return [target_node]

def setup(app):
    app.add_role('docref', role_docref)
    app.add_directive('duplabel', DupLabelDirective)
