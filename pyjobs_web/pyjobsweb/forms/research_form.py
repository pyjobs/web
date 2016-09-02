# -*- coding: utf-8 -*-
import tw2.core as twc
import tw2.forms as twf
import tw2.jqplugins.select2 as twsel


class GeocompleteField(twsel.Select2AjaxSingleSelectField):
    def __init__(self, **kwargs):
        super(GeocompleteField, self).__init__(**kwargs)

    attrs = dict(style='width: 100%;')
    options = []
    opts = dict(
        placeholder=u'Rechercher une localisation...',
        minimumInputLength=1,
        maximumInputLength=125,
        allowClear=True,
        ajax=dict(
            url='/geocomplete',
            dataType='json',
            type='POST',
            quietMillis=100,
            cache=True,
            data=twc.js_callback(
                """
                function(term) {
                    return {address: term};
                }
                """
            ),
            results=twc.js_callback(
                """
                function(data) {
                    var results = [];

                    if ('results' in data) {
                        $.each(data['results'], function(i, v) {
                            var o = {};
                            o.id = v['to_submit'];
                            o.name = v['to_display'];
                            o.value = v['to_display'];
                            results.push(o);
                        });
                    }

                    return {
                        results: results
                    };
                }
                """
            )
        ),
        escapeMarkup=twc.js_callback(
            """
            function(markup) {
                return markup;
            }
            """
        ),
        formatResult=twc.js_callback(
            """
            function(location) {
                var markup = '<option value="' + location.value + '">'
                    + location.name
                    + '</option>';
                return markup;
            }
            """
        ),
        formatSelection=twc.js_callback(
            """
            function(location) {
                return location.value || location.text
            }
            """
        )
    )


class ResearchForm(twf.Form):
    class child(twf.widgets.BaseLayout):
        inline_engine_name = "mako"
        template = \
            u'''
            % for c in w.children_hidden:
                ${c.display()}
            % endfor

            <%def name="display_field(field, css_class)">
                <div class="${css_class}">
                    <label class="sr-only control-label" for="${field.compound_id}">
                        ${field.label}
                    </label>
                    ${field.display()}
                </div>
                <div class="hidden-md hidden-lg col-xs-12" style="height:7px;"></div>
            </%def>

            ${display_field(w.children.query, 'col-xs-12 col-md-4 col-lg-4')}
            ${display_field(w.children.center, 'col-xs-12 col-md-3 col-lg-3')}
            ${display_field(w.children.radius, 'col-xs-12 col-md-3 col-lg-3')}

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
            placeholder=u"Mots clés recherchés...",
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
            name="center",
            label=u'Autour de :'
        )

        distances = [
            "5", "10", "25", "50", "100", "200", "200+"
        ]
        tmp_options = []
        for i, d in enumerate(distances):
            distances_km = "{}{}".format(d, "km")
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
            placeholder=u'Distance maximale',
            opts=dict(
                allowClear=True,
            )
        )

    def __init__(self, **kwargs):
        super(ResearchForm, self).__init__(**kwargs)
        self.submit = None
        self.css_class = 'row'
