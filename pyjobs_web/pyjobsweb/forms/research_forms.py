# -*- coding: utf-8 -*
import tw2.core as twc
import tw2.forms as twf
import tw2.jqplugins.select2 as twsel
from tw2.core.validation import Validator

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
                <button type="submit" class="btn btn-default btn-sm" style="width: 100%;">
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

                ],
                maximumSelectionSize=10,
                tokenSeparators=[','],
                initSelection=twc.js_callback(
                    '''
                    function (element, callback) {
                        var init_data = [];

                        query = params['query'];

                        if(typeof query !== "undefined" && query) {
                            $.each(query.split(','), function(i, v) {
                                var elem = {};
                                elem.id = v;
                                elem.text = v;
                                init_data.push(elem);
                            });
                        }

                        callback(init_data);
                    }
                    '''
                )
            ),
            ondemand=True,
            validator=Validator()
        )

        center = GeocompleteField(
            resources=[],
            name='center',
            label=u'Autour de :'
        )

        distances = [
            '5', '10', '25', '50', '100', '200'
        ]
        tmp_options = [(d, '{}{}'.format(d, 'km')) for d in distances]

        radius = twsel.Select2SingleSelectField(
            resources=[],
            name='radius',
            label=u'Dans un rayon de :',
            options=tmp_options,
            value='',
            attrs=dict(style='width: 100%;'),
            placeholder=u"Et jusqu'à...",
            opts=dict(
                allowClear=True,
                initSelection=twc.js_callback(
                    '''
                    function (element, callback) {
                        var init_data;

                        radius = params['radius'];

                        if(typeof radius !== "undefined" && radius) {
                            var elem = {};
                            elem.id = radius;
                            elem.text = radius.concat('km');
                            init_data = elem;
                        }

                        callback(init_data);
                    }
                    '''
                )
            ),
            ondemand=True,
            validator=Validator()
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
                allowClear=True,
                initSelection=twc.js_callback(
                    '''
                    function (element, callback) {
                        var init_data;

                        sort_by = params['sort_by'];

                        if(typeof sort_by !== "undefined" && sort_by) {
                            var elem = {};
                            elem.id = sort_by;

                            if(sort_by === 'dates') {
                                elem.text = 'Dates';
                            } else {
                                elem.text = 'Pertinence';
                            }

                            init_data = elem;
                        }

                        callback(init_data);
                    }
                    '''
                )
            ),
            ondemand=True,
            validator=Validator()
        )

    def __init__(self, **kwargs):
        super(JobsResearchForm, self).__init__(**kwargs)
        self.submit = None
        self.method = 'GET'
        self.attrs = {'enctype': 'application/x-www-form-urlencoded'}
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
                <button type="submit" class="btn btn-default btn-sm" style="width: 100%;">
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

                ],
                maximumSelectionSize=10,
                tokenSeparators=[','],
                initSelection=twc.js_callback(
                    '''
                    function (element, callback) {
                        var init_data = [];

                        query = params['query'];

                        if(typeof query !== "undefined" && query) {
                            $.each(query.split(','), function(i, v) {
                                var elem = {};
                                elem.id = v;
                                elem.text = v;
                                init_data.push(elem);
                            });
                        }

                        callback(init_data);
                    }
                    '''
                )
            ),
            ondemand=True,
            validator=Validator()
        )

        center = GeocompleteField(
            resources=[],
            name='center',
            label=u'Autour de :'
        )

        distances = [
            '5', '10', '25', '50', '100', '200'
        ]
        tmp_options = [(d, '{}{}'.format(d, 'km')) for d in distances]

        radius = twsel.Select2SingleSelectField(
            resources=[],
            name='radius',
            label=u'Dans un rayon de :',
            options=tmp_options,
            value='',
            attrs=dict(style='width: 100%;'),
            placeholder=u"Et jusqu'à...",
            opts=dict(
                allowClear=True,
                initSelection=twc.js_callback(
                    '''
                    function (element, callback) {
                        var init_data;

                        radius = params['radius'];

                        if(typeof radius !== "undefined" && radius) {
                            var elem = {};
                            elem.id = radius;
                            elem.text = radius.concat('km');
                            init_data = elem;
                        }

                        callback(init_data);
                    }
                    '''
                )
            ),
            ondemand=True,
            validator=Validator()
        )

    def __init__(self, **kwargs):
        super(CompaniesResearchForm, self).__init__(**kwargs)
        self.submit = None
        self.method = 'GET'
        self.attrs = {'enctype': 'application/x-www-form-urlencoded'}
        self.css_class = 'row'
