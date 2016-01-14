# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1452763619.199141
_enable_loop = True
_template_filename = u'/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/master.mak'
_template_uri = u'/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/master.mak'
_source_encoding = 'utf-8'
from markupsafe import escape_silent as escape
_exports = ['footer', 'body_class', 'head_content', 'meta', 'title', 'main_menu', 'content_wrapper']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        tg = context.get('tg', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<!DOCTYPE html>\n<html>\n<head>\n    ')
        __M_writer(escape(self.meta()))
        __M_writer(u'\n    <title>')
        __M_writer(escape(self.title()))
        __M_writer(u'</title>\n    <link rel="stylesheet" type="text/css" media="screen" href="')
        __M_writer(escape(tg.url('/css/bootstrap.min.css')))
        __M_writer(u'" />\n    <link rel="stylesheet" type="text/css" media="screen" href="')
        __M_writer(escape(tg.url('/css/style.css')))
        __M_writer(u'" />\n    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">\n    ')
        __M_writer(escape(self.head_content()))
        __M_writer(u'\n</head>\n<body class="')
        __M_writer(escape(self.body_class()))
        __M_writer(u'">\n    ')
        __M_writer(escape(self.main_menu()))
        __M_writer(u'\n  <div class="container">\n    ')
        __M_writer(escape(self.content_wrapper()))
        __M_writer(u'\n  </div>\n    ')
        __M_writer(escape(self.footer()))
        __M_writer(u'\n  <script src="http://code.jquery.com/jquery.js"></script>\n  <script src="')
        __M_writer(escape(tg.url('/javascript/bootstrap.min.js')))
        __M_writer(u'"></script>\n</body>\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        __M_writer(u'\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        tg = context.get('tg', UNDEFINED)
        getattr = context.get('getattr', UNDEFINED)
        tmpl_context = context.get('tmpl_context', UNDEFINED)
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n  <footer class="footer hidden-xs hidden-sm">\n    <a class="pull-right" href="http://www.turbogears.org"><img style="vertical-align:middle;" src="')
        __M_writer(escape(tg.url('/img/under_the_hood_blue.png')))
        __M_writer(u'" alt="TurboGears 2" /></a>\n    <p>Copyright &copy; ')
        __M_writer(escape(getattr(tmpl_context, 'project_name', 'TurboGears2')))
        __M_writer(u' ')
        __M_writer(escape(h.current_year()))
        __M_writer(u'</p>\n  </footer>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_body_class(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head_content(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_meta(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        response = context.get('response', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n  <meta charset="')
        __M_writer(escape(response.charset))
        __M_writer(u'" />\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'  ')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_main_menu(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        tg = context.get('tg', UNDEFINED)
        request = context.get('request', UNDEFINED)
        page = context.get('page', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n  <!-- Navbar -->\n  <nav class="navbar navbar-default">\n    <div class="navbar-header">\n      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar-content">\n        <span class="sr-only">Toggle navigation</span>\n        <span class="icon-bar"></span>\n        <span class="icon-bar"></span>\n        <span class="icon-bar"></span>\n      </button>\n      <a class="navbar-brand" href="')
        __M_writer(escape(tg.url('/')))
        __M_writer(u'">\n        <img src="')
        __M_writer(escape(tg.url('/img/pyjobs_logo_square.png')))
        __M_writer(u'" style="height: 32px;" alt="TurboGears 2"/>\n        pyjobs &mdash; <small>jobs python et recrutement, pour tous</small>\n      </a>\n    </div>\n\n    <div class="collapse navbar-collapse" id="navbar-content">\n      <ul class="nav navbar-nav">\n\n<!--\n       <li class="')
        __M_writer(escape(('', 'active')[page=='index']))
        __M_writer(u'"><a href="')
        __M_writer(escape(tg.url('/recruteurs')))
        __M_writer(u'">Recruteurs</a></li>\n        <li class="')
        __M_writer(escape(('', 'active')[page=='about']))
        __M_writer(u'"><a href="')
        __M_writer(escape(tg.url('/candidats')))
        __M_writer(u'">Candidats</a></li>\n        <li class="')
        __M_writer(escape(('', 'active')[page=='data']))
        __M_writer(u'"><a href="')
        __M_writer(escape(tg.url('/about')))
        __M_writer(u'">A propos</a></li>\n-->\n      </ul>\n\n')
        if tg.auth_stack_enabled:
            __M_writer(u'      <ul class="nav navbar-nav navbar-right">\n        <li class="')
            __M_writer(escape(('', 'active')[page=='index']))
            __M_writer(u'"><a href="')
            __M_writer(escape(tg.url('/recruteurs')))
            __M_writer(u'">Recruteurs</a></li>\n        <li class="')
            __M_writer(escape(('', 'active')[page=='about']))
            __M_writer(u'"><a href="')
            __M_writer(escape(tg.url('/candidats')))
            __M_writer(u'">Candidats</a></li>\n        <li class="')
            __M_writer(escape(('', 'active')[page=='index']))
            __M_writer(u'"><a href="')
            __M_writer(escape(tg.url('/recruteurs')))
            __M_writer(u'">Sources</a></li>\n        <li class="')
            __M_writer(escape(('', 'active')[page=='data']))
            __M_writer(u'"><a href="')
            __M_writer(escape(tg.url('/about')))
            __M_writer(u'">A propos</a></li>\n')
            if not request.identity:
                __M_writer(u'        <li><a href="')
                __M_writer(escape(tg.url('/login')))
                __M_writer(u'">Login</a></li>\n')
            else:
                __M_writer(u'        <li><a href="')
                __M_writer(escape(tg.url('/logout_handler')))
                __M_writer(u'">Logout</a></li>\n        <li><a href="')
                __M_writer(escape(tg.url('/admin')))
                __M_writer(u'">Admin</a></li>\n')
            __M_writer(u'      </ul>\n')
        __M_writer(u'    </div>\n  </nav>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content_wrapper(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        tg = context.get('tg', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n  ')

        flash=tg.flash_obj.render('flash', use_js=False)
          
        
        __M_writer(u'\n')
        if flash:
            __M_writer(u'      <div class="row">\n        <div class="col-md-8 col-md-offset-2">\n              ')
            __M_writer(flash )
            __M_writer(u'\n        </div>\n      </div>\n')
        __M_writer(u'  ')
        __M_writer(escape(self.body()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"17": 0, "24": 1, "25": 4, "26": 4, "27": 5, "28": 5, "29": 6, "30": 6, "31": 7, "32": 7, "33": 9, "34": 9, "35": 11, "36": 11, "37": 12, "38": 12, "39": 14, "40": 14, "41": 16, "42": 16, "43": 18, "44": 18, "45": 33, "46": 35, "47": 39, "48": 40, "49": 42, "50": 49, "51": 93, "57": 44, "65": 44, "66": 46, "67": 46, "68": 47, "69": 47, "70": 47, "71": 47, "77": 35, "86": 40, "95": 36, "100": 36, "101": 37, "102": 37, "108": 42, "112": 42, "118": 51, "125": 51, "126": 61, "127": 61, "128": 62, "129": 62, "130": 71, "131": 71, "132": 71, "133": 71, "134": 72, "135": 72, "136": 72, "137": 72, "138": 73, "139": 73, "140": 73, "141": 73, "142": 77, "143": 78, "144": 79, "145": 79, "146": 79, "147": 79, "148": 80, "149": 80, "150": 80, "151": 80, "152": 81, "153": 81, "154": 81, "155": 81, "156": 82, "157": 82, "158": 82, "159": 82, "160": 83, "161": 84, "162": 84, "163": 84, "164": 85, "165": 86, "166": 86, "167": 86, "168": 87, "169": 87, "170": 89, "171": 91, "177": 21, "183": 21, "184": 22, "188": 24, "189": 25, "190": 26, "191": 28, "192": 28, "193": 32, "194": 32, "195": 32, "201": 195}, "uri": "/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/master.mak", "filename": "/home/bastien/Projects/pyjobs_web/pyjobs_web/pyjobsweb/templates/master.mak"}
__M_END_METADATA
"""
