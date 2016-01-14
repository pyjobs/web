# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1452763619.172057
_enable_loop = True
_template_filename = '/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/index.mak'
_template_uri = '/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/index.mak'
_source_encoding = 'utf-8'
from markupsafe import escape_silent as escape
_exports = ['title']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'local:templates.master', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n  <div class="row">\n    <div class="col-md-8">\n      <div class="jumbotron">\n        <h1>Welcome to TurboGears 2.3</h1>\n        <p>If you see this page it means your installation was successful!</p>\n        <p>TurboGears 2 is rapid web application development toolkit designed to make your life easier.</p>\n        <p>\n          <a class="btn btn-primary btn-lg" href="http://www.turbogears.org" target="_blank">\n            ')
        __M_writer(escape(h.icon('book')))
        __M_writer(u' Learn more\n          </a>\n        </p>\n      </div>\n    </div>\n    <div class="col-md-4 hidden-xs hidden-sm">\n      <a class="btn btn-info btn-sm active" href="http://turbogears.readthedocs.org/en/latest">')
        __M_writer(escape(h.icon('book')))
        __M_writer(u' TG2 Documentation</a> <span class="label label-success">new</span><em> Get Started</em><br/>\n        <br/>\n      <a class="btn btn-info btn-sm active" href="http://turbogears.readthedocs.org/en/latest/cookbook/cookbook.html">')
        __M_writer(escape(h.icon('book')))
        __M_writer(u' TG2 CookBook</a><em> Read the Cookbook</em> <br/>\n        <br/>\n      <a class="btn btn-info btn-sm active" href="http://groups.google.com/group/turbogears">')
        __M_writer(escape(h.icon('comment')))
        __M_writer(u' Join the Mail List</a> <em>for help/discussion</em><br/>\n        <br/>\n      <a class="btn btn-info btn-sm active" href="http://runnable.com/TurboGears">')
        __M_writer(escape(h.icon('play')))
        __M_writer(u' Play on Runnable</a> <em>for basic examples</em><br/>\n        <br/>\n      <a class="btn btn-info btn-sm active" href="http://stackoverflow.com/questions/tagged/turbogears2">')
        __M_writer(escape(h.icon('search')))
        __M_writer(u' Search Stackoverflow</a> <em>for questions</em>\n    </div>\n  </div>\n\n  <div class="row">\n    <div class="col-md-4">\n      <h3>Code your data model</h3>\n      <p> Design your data <code>model</code>, Create the database, and Add some bootstrap data.</p>\n    </div>\n\n    <div class="col-md-4">\n      <h3>Design your URL architecture</h3>\n      <p> Decide your URLs, Program your <code>controller</code> methods, Design your\n        <code>templates</code>, and place some static files (CSS and/or Javascript). </p>\n    </div>\n\n    <div class="col-md-4">\n      <h3>Distribute your app</h3>\n      <p> Test your source, Generate project documents, Build a distribution.</p>\n    </div>\n  </div>\n\n  <em class="pull-right small"> Thank you for choosing TurboGears.</em>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n  Welcome to TurboGears 2.3, standing on the shoulders of giants, since 2007\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"34": 1, "35": 5, "36": 14, "37": 14, "38": 20, "39": 20, "40": 22, "41": 22, "42": 24, "43": 24, "44": 26, "45": 26, "46": 28, "47": 28, "53": 3, "57": 3, "28": 0, "63": 57}, "uri": "/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/index.mak", "filename": "/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/index.mak"}
__M_END_METADATA
"""
