# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1452783200.83026
_enable_loop = True
_template_filename = '/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/job.mak'
_template_uri = '/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/job.mak'
_source_encoding = 'utf-8'
from markupsafe import escape_silent as escape
_exports = []


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
        job = context.get('job', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n<h1>\n    ')
        __M_writer(escape(job.title))
        __M_writer(u'\n\n')
        for tag in job.alltags:
            __M_writer(u'        <span class="label label-default ')
            __M_writer(escape(tag.css))
            __M_writer(u'">')
            __M_writer(escape(tag.tag))
            __M_writer(u'</span>\n')
        __M_writer(u'\n')
        for tag in job.condition_tags:
            __M_writer(u'        <span class="label label-default ')
            __M_writer(escape(tag.css))
            __M_writer(u'">')
            __M_writer(escape(tag.tag))
            __M_writer(u'</span>\n')
        __M_writer(u'</h1>\n\n<p class="lead job_content">\n\n    <span class="published">\n        ')
        __M_writer(escape(job.published))
        __M_writer(u'\n    </span>\n\n    -\n\n    <span class="company">\n')
        if job.company_url:
            __M_writer(u'            <a href="')
            __M_writer(escape(job.company_url))
            __M_writer(u'" title="Site internet de ')
            __M_writer(escape(job.company))
            __M_writer(u'">\n                ')
            __M_writer(escape(job.company))
            __M_writer(u'\n            </a>\n')
        else:
            __M_writer(u'            ')
            __M_writer(escape(job.company))
            __M_writer(u'\n')
        __M_writer(u'    </span>\n\n</p>\n\n<p>\n    ')
        __M_writer(job.description)
        __M_writer(u'\n</p>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "34": 1, "35": 4, "36": 4, "37": 6, "38": 7, "39": 7, "40": 7, "41": 7, "42": 7, "43": 9, "44": 10, "45": 11, "46": 11, "47": 11, "48": 11, "49": 11, "50": 13, "51": 18, "52": 18, "53": 24, "54": 25, "55": 25, "56": 25, "57": 25, "58": 25, "59": 26, "60": 26, "61": 28, "62": 29, "63": 29, "64": 29, "65": 31, "66": 36, "67": 36, "73": 67}, "uri": "/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/job.mak", "filename": "/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/job.mak"}
__M_END_METADATA
"""
