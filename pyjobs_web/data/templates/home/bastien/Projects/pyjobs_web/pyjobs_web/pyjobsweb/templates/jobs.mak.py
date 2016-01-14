# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1452764038.481002
_enable_loop = True
_template_filename = '/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/jobs.mak'
_template_uri = '/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/jobs.mak'
_source_encoding = 'utf-8'
from markupsafe import escape_silent as escape
_exports = ['job_pagination', 'title']



import urllib

def encode_object(value):
    if type(value) in (str, unicode):
        return value.encode('utf-8')



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
        loop = __M_loop = runtime.LoopStack()
        h = context.get('h', UNDEFINED)
        def job_pagination():
            return render_job_pagination(context._locals(__M_locals))
        jobs = context.get('jobs', UNDEFINED)
        sources = context.get('sources', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n    <div class="row">\n        <div class="col-md-12">\n            <div class="page-header">\n                <h1>\n                    Le job qu\'il vous faut &mdash; en python\n                    <div class="btn-group pull-right" role="group">\n                        <button type="button" class="btn btn-default"><i class="fa fa-3x fa-twitter" style="color: #55ACEE;"></i></button>\n                        <button type="button" class="btn btn-warning"><i class="fa fa-3x fa-rss"></i></button>\n                    </div>\n\n                </h1>\n')
        __M_writer(u'            </div>\n        </div>\n    </div>\n\n')
        __M_writer(escape(job_pagination()))
        __M_writer(u'\n\n')
        loop = __M_loop._enter(jobs)
        try:
            for job in loop:
                __M_writer(u'\n        <!-- Modal -->\n        <div class="modal" id="modal-job-')
                __M_writer(escape(job.id))
                __M_writer(u'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">\n          <div class="modal-dialog modal-lg" role="document">\n            <div class="modal-content">\n              <div class="modal-header">\n                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\n                <h4 class="modal-title" id="myModalLabel">')
                __M_writer(escape(job.title))
                __M_writer(u'</h4>\n              </div>\n              <div class="modal-body">\n                  <ul>\n                      <li>')
                __M_writer(escape(job.company))
                __M_writer(u'</li>\n                      <li>')
                __M_writer(escape(job.address))
                __M_writer(u'</li>\n                  </ul>\n                  <hr/>\n                  ')
                __M_writer(job.description)
                __M_writer(u'\n              </div>\n              <div class="modal-footer">\n                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\n                <button type="button" class="btn btn-primary">Save changes</button>\n              </div>\n            </div>\n          </div>\n        </div>\n\n        <div class="row">\n            <div class="col-md-12">\n                <div id="job-post-')
                __M_writer(escape(job.id))
                __M_writer(u'" class="job-item ')
                __M_writer(escape(loop.cycle('row-even', 'row-odd')))
                __M_writer(u'" style="border-top: 1px dotted #DDD; padding: 1em 1em 3em 1em;">\n                    <div class="row" id="job-post-head-')
                __M_writer(escape(job.id))
                __M_writer(u'">\n                        <div class="col-md-9">\n                            <h2 style="margin-top: 0; padding-top: 0; font-size: 1.7em;">\n                                <a style="color: #555; font-weight: bold;" data-toggle="modal" data-target="#modal-job-')
                __M_writer(escape(job.id))
                __M_writer(u'" >')
                __M_writer(escape(job.title))
                __M_writer(u'</a>\n\n                                <!-- TODO: TurboGears "url" helper ? -->\n                                <a href="/job/')
                __M_writer(escape(job.id))
                __M_writer(u'/')
                __M_writer(escape(h.slugify(job.title)))
                __M_writer(u'">\n                                    JOB PAGE\n                                </a>\n\n')
                for tag in job.condition_tags:
                    __M_writer(u'                                    <span class="label label-default ')
                    __M_writer(escape(tag.css))
                    __M_writer(u'">')
                    __M_writer(escape(tag.tag))
                    __M_writer(u'</span>\n')
                __M_writer(u'\n                                <br/>\n                                <div style="color: #999;">')
                __M_writer(escape(job.company))
                __M_writer(u'</div>\n                            </h2>\n                        </div>\n\n                        <div class="col-md-3">\n                            <div class="text-right">\n                                <span style="font-size: 1.5em; font-weight: bold; color: #777;">')
                __M_writer(escape(job.published))
                __M_writer(u'</span><br/>\n                                <a href="')
                __M_writer(escape(sources[job.source].url))
                __M_writer(u'" style="color: #AAA; font-weight: bold;">\n                                    ')
                __M_writer(escape(sources[job.source].label))
                __M_writer(u'<br/>\n                                    <img style="max-height: 32px;" src="')
                __M_writer(escape(sources[job.source].logo_url))
                __M_writer(u'" alt="')
                __M_writer(escape(sources[job.source].label))
                __M_writer(u'"/>\n                                </a>\n\n                            </div>\n                        </div>\n                    </div>\n                    <div class="row" id="job-post-detail-')
                __M_writer(escape(job.id))
                __M_writer(u'-detail">\n')
                __M_writer(u'                        <div class="col-md-12">\n')
                for tag in job.alltags:
                    __M_writer(u'                                <span class="label label-default label-pyjob">')
                    __M_writer(escape(tag.tag))
                    __M_writer(u'</span>\n')
                __M_writer(u'                        </div>\n')
                __M_writer(u'                    </div>\n')
                __M_writer(u'                </div>\n            </div>\n            <div class="col-md-3">\n            </div>\n        </div>\n')
        finally:
            loop = __M_loop._exit()
        __M_writer(u'\n')
        __M_writer(escape(job_pagination()))
        __M_writer(u'\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_job_pagination(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        tmpl_context = context.get('tmpl_context', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'    <div class="row">\n        <div class="col-md-12">\n            <ul class="pagination">\n                ')
        __M_writer(escape(tmpl_context.paginators.jobs.pager(format='$link_first $link_previous <li><span>Page $page / $page_count</span></li> $link_next $link_last', page_link_template='<li><a %s>%s</a></li>', page_plain_template='<li><span%s>%s</span></li>', symbol_first=u'<< début', symbol_last=u'fin >>', symbol_previous=u'< précédente', symbol_next=u'suivante >', show_if_single_page=True)))
        __M_writer(u'\n            </ul>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\nLearning TurboGears 2.3: Quick guide to the Quickstart pages.\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"128": 15, "129": 15, "135": 21, "145": 139, "139": 21, "17": 2, "37": 0, "48": 1, "49": 9, "50": 19, "51": 23, "52": 54, "53": 58, "54": 58, "55": 60, "58": 61, "59": 63, "60": 63, "61": 68, "62": 68, "63": 72, "64": 72, "65": 73, "66": 73, "67": 76, "68": 76, "69": 88, "70": 88, "71": 88, "72": 88, "73": 89, "74": 89, "75": 92, "76": 92, "77": 92, "78": 92, "79": 95, "80": 95, "81": 95, "82": 95, "83": 99, "84": 100, "85": 100, "86": 100, "87": 100, "88": 100, "89": 102, "90": 104, "91": 104, "92": 110, "93": 110, "94": 111, "95": 111, "96": 112, "97": 112, "98": 113, "99": 113, "100": 113, "101": 113, "102": 119, "103": 119, "104": 123, "105": 124, "106": 125, "107": 125, "108": 125, "109": 127, "110": 133, "111": 137, "114": 143, "115": 144, "116": 144, "122": 11, "127": 12}, "uri": "/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/jobs.mak", "filename": "/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/jobs.mak"}
__M_END_METADATA
"""
