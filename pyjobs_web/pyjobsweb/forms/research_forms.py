# -*- coding: utf-8 -*-
import tw2.forms as twf
import tw2.jqplugins.select2 as twsel

from pyjobsweb.forms.custom_widgets import GeocompleteField


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
                <button type="submit" class="form-control btn btn-default">
                    Filtrer
                    <i class="fa fa-1x fa-search"></i>
                </button>
            </div>
            '''

        query = twsel.Select2MultipleSelectField(
            resources=[],
            name='query',
            label=u'Mot clés :',
            options=[],
            value='',
            attrs=dict(style='width: 100%;'),
            placeholder=u'Mots clés recherchés...',
            opts=dict(
                tags=[
                    'Python', 'Django', 'Flask', 'Pyramid', 'Turbogears'
                ],
                maximumSelectionSize=10,
                tokenSeparators=[',']
            ),
            ondemand=True
        )

        center = GeocompleteField(
            resources=[],
            name='center',
            label=u'Autour de :'
        )

        distances = [
            '5', '10', '25', '50', '100', '200', '200+'
        ]
        tmp_options = []
        for i, d in enumerate(distances):
            distances_km = '{}{}'.format(d, 'km')
            if i == len(distances) - 1:
                option = ('infty', distances_km)
            else:
                option = (d, distances_km)

            tmp_options.append(option)

        radius = twsel.Select2SingleSelectField(
            resources=[],
            name='radius',
            label=u'Dans un rayon de :',
            options=tmp_options,
            value='',
            attrs=dict(style='width: 100%;'),
            placeholder=u"Et jusqu'à...",
            opts=dict(
                allowClear=True
            )
        )

        sort_by = twsel.Select2SingleSelectField(
            resources=[],
            name='sort_by',
            label=u'Trier par :',
            options=[('dates', 'Dates'), ('scores', 'Pertinence')],
            value='',
            attrs=dict(style='width: 100%;'),
            placeholder=u"Trier par...",
            opts=dict(
                allowClear=True
            )
        )

    def __init__(self, **kwargs):
        super(JobsResearchForm, self).__init__(**kwargs)
        self.submit = None
        self.css_class = 'row'


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
                <button type="submit" class="form-control btn btn-default">
                    Filtrer
                    <i class="fa fa-1x fa-search"></i>
                </button>
            </div>
            '''

        query = twsel.Select2MultipleSelectField(
            resources=[],
            name='query',
            label=u'Mot clés :',
            options=[],
            value='',
            attrs=dict(style='width: 100%;'),
            placeholder=u'Mots clés recherchés...',
            opts=dict(
                tags=[
                    'Python', 'Django', 'Flask', 'Pyramid', 'Turbogears'
                ],
                maximumSelectionSize=10,
                tokenSeparators=[',']
            ),
            ondemand=True
        )

        center = GeocompleteField(
            resources=[],
            name='center',
            label=u'Autour de :'
        )

        distances = [
            '5', '10', '25', '50', '100', '200', '200+'
        ]
        tmp_options = []
        for i, d in enumerate(distances):
            distances_km = '{}{}'.format(d, 'km')
            if i == len(distances) - 1:
                option = ('infty', distances_km)
            else:
                option = (d, distances_km)

            tmp_options.append(option)

        radius = twsel.Select2SingleSelectField(
            resources=[],
            name='radius',
            label=u'Dans un rayon de :',
            options=tmp_options,
            value='',
            attrs=dict(style='width: 100%;'),
            placeholder=u"Et jusqu'à...",
            opts=dict(
                allowClear=True
            )
        )

    def __init__(self, **kwargs):
        super(CompaniesResearchForm, self).__init__(**kwargs)
        self.submit = None
        self.css_class = 'row'