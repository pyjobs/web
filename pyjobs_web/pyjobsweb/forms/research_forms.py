# -*- coding: utf-8 -*
import tw2.forms as twf

from pyjobsweb.forms.custom_widgets import PersistentSelect2SingleSelect
from pyjobsweb.forms.custom_widgets import PersistentSelect2MultipleSelect
from pyjobsweb.forms.custom_widgets import GeocompleteField


def _get_distances():
    distances = ['5', '10', '25', '50', '100', '200']
    return [(d, '{}{}'.format(d, 'km')) for d in distances]


def _get_keyword_list():
    return [
        'Python',
        'Django',
        'Flask',
        'Pyramid',
        'Turbogears',
        'Ansible',
        'Plone',
        'Docker',
        'PostgreSQL',
        'MySQL',
        'Oracle',
        'Startup',
        'CTO',
        'Devops'
    ]


class JobsResearchForm(twf.Form):
    class child(twf.widgets.BaseLayout):
        inline_engine_name = "mako"
        template = \
            u'''
            % for c in w.children_hidden:
                ${c.display()}
            % endfor

            <div class="col-xs-12 col-md-3 col-lg-3">
                <label class="sr-only control-label" for="${w.children.query.compound_id}">
                    ${w.children.query.label}
                </label>
                ${w.children.query.display()}
            </div>
            <div class="hidden-md hidden-lg col-xs-12" style="height:7px;"></div>

            <div class="col-xs-12 col-md-3 col-lg-3">
                <label class="sr-only control-label" for="${w.children.center.compound_id}">
                    ${w.children.center.label}
                </label>
                ${w.children.center.display()}
            </div>
            <div class="hidden-md hidden-lg col-xs-12" style="height:7px;"></div>

            <div class="col-xs-12 col-md-2 col-lg-2">
                <label class="sr-only control-label" for="${w.children.radius.compound_id}">
                    ${w.children.radius.label}
                </label>
                ${w.children.radius.display()}
            </div>
            <div class="hidden-md hidden-lg col-xs-12" style="height:7px;"></div>

            <div class="col-xs-12 col-md-2 col-lg-2">
                <label class="sr-only control-label" for="${w.children.sort_by.compound_id}">
                    ${w.children.sort_by.label}
                </label>
                ${w.children.sort_by.display()}
            </div>
            <div class="hidden-md hidden-lg col-xs-12" style="height:7px;"></div>

            <div class="col-xs-12 col-md-2 col-lg-2">
                <button type="submit" class="btn btn-default btn-sm" style="width: 100%;">
                    Filtrer
                    <i class="fa fa-1x fa-search"></i>
                </button>
            </div>
            '''

        query = PersistentSelect2MultipleSelect(
            name='query',
            label=u'Mot clés :',
            options=_get_keyword_list(),
            value='',
            placeholder=u'Mots clés recherchés...',
            attrs=dict(style='width: 100%;')
        )

        center = GeocompleteField(
            name='center',
            label=u'Autour de :',
            value='',
            placeholder=u'Autour de...',
            attrs=dict(style='width: 100%;')
        )

        radius = PersistentSelect2SingleSelect(
            name='radius',
            label=u'Dans un rayon de :',
            options=_get_distances(),
            value='',
            placeholder=u"Et jusqu'à...",
            attrs=dict(style='width: 100%;')
        )

        sort_by = PersistentSelect2SingleSelect(
            name='sort_by',
            label=u'Trier par :',
            options=[('dates', 'Dates'), ('scores', 'Pertinence')],
            value='',
            attrs=dict(style='width: 100%;'),
            placeholder=u"Trier par..."
        )

    def __init__(self, **kwargs):
        super(JobsResearchForm, self).__init__(**kwargs)
        self.submit = None
        self.method = 'GET'
        self.attrs = {'enctype': 'application/x-www-form-urlencoded'}
        self.css_class = 'row'
        self.action = '/jobs/search'


class CompaniesResearchForm(twf.Form):
    class child(twf.widgets.BaseLayout):
        inline_engine_name = "mako"
        template = \
            u'''
            % for c in w.children_hidden:
                ${c.display()}
            % endfor

            <div class="col-xs-12 col-md-4 col-lg-4">
                <label class="sr-only control-label" for="${w.children.query.compound_id}">
                    ${w.children.query.label}
                </label>
                ${w.children.query.display()}
            </div>
            <div class="hidden-md hidden-lg col-xs-12" style="height:7px;"></div>

            <div class="col-xs-12 col-md-4 col-lg-4">
                <label class="sr-only control-label" for="${w.children.center.compound_id}">
                    ${w.children.center.label}
                </label>
                ${w.children.center.display()}
            </div>
            <div class="hidden-md hidden-lg col-xs-12" style="height:7px;"></div>

            <div class="col-xs-12 col-md-2 col-lg-2">
                <label class="sr-only control-label" for="${w.children.radius.compound_id}">
                    ${w.children.radius.label}
                </label>
                ${w.children.radius.display()}
            </div>
            <div class="hidden-md hidden-lg col-xs-12" style="height:7px;"></div>

            <div class="col-xs-12 col-md-2 col-lg-2">
                <button type="submit" class="btn btn-default btn-sm" style="width: 100%;">
                    Filtrer
                    <i class="fa fa-1x fa-search"></i>
                </button>
            </div>
            '''

        query = PersistentSelect2MultipleSelect(
            name='query',
            label=u'Mot clés :',
            options=_get_keyword_list(),
            value='',
            placeholder=u'Mots clés recherchés...',
            attrs=dict(style='width: 100%;')
        )

        center = GeocompleteField(
            name='center',
            label=u'Autour de :',
            value='',
            placeholder=u'Autour de...',
            attrs=dict(style='width: 100%;')
        )

        radius = PersistentSelect2SingleSelect(
            name='radius',
            label=u'Dans un rayon de :',
            options=_get_distances(),
            value='',
            placeholder=u"Et jusqu'à...",
            attrs=dict(style='width: 100%;')
        )

    def __init__(self, **kwargs):
        super(CompaniesResearchForm, self).__init__(**kwargs)
        self.submit = None
        self.method = 'GET'
        self.attrs = {'enctype': 'application/x-www-form-urlencoded'}
        self.css_class = 'row'
        self.action = '/societes-qui-recrutent/search'
