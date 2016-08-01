# -*- coding: utf-8 -*-
import tw2.core as twc
import tw2.forms as twf
import tw2.jqplugins.select2 as twsel


class GeocompleteField(twsel.Select2AjaxSingleSelectField):
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
        ),
        formatInputTooShort=twc.js_callback(
            """
            function(a, b) {
                var c = b - a.length;
                return 'Veuillez saisir ' + c + ' caract\\xE8re(s) '
                    + 'suppl\\xE9mentaire(s).';
            }
            """
        ),
        formatInputTooLong=twc.js_callback(
            """
            function(a, b) {
                return 'Saisie trop longue.';
            }
            """
        ),
        formatSearching=twc.js_callback(
            """
            function() {
                return 'Recherche en cours...';
            }
            """
        ),
        formatNoMatches=twc.js_callback(
            """
            function() {
                return 'Aucun r\\xE9sultat ne correpond \\xE0 votre recherche.';
            }
            """
        )
    )


class ResearchForm(twf.Form):
    class child(twf.widgets.BaseLayout):
        inline_engine_name = "mako"
        template = \
            u'''
            <h2>Rechercher une offre d'emploi</h2>
            <div class="form-group">
                <label class="control-label col-sm-2" for="query">Requête :</label>
                <div class="col-xs-10 col-sm-10">
                    ${w.children.query.display()|n}
                </div>
            </div>
            <div class="col-xs-12" style="height:3px;"></div>
            <div class="form-group">
                <label class="control-label col-sm-2" for="center">Autour de :</label>
                <div class="col-xs-10 col-sm-10">
                    ${w.children.center.display()|n}
                </div>
            </div>
            <div class="col-xs-12" style="height:3px;"></div>
            <div class="form-group">
                <label class="control-label col-sm-2" for="radius">Dans un rayon de :</label>
                <div class="col-xs-10 col-sm-10">
                    ${w.children.radius.display()|n}
                </div>
            </div>
            <div class="col-xs-12" style="height:3px;"></div>
            <div class="form-group">
                <label class="control-label col-sm-2" for="submit"> </label>
                <div class="col-xs-10 col-md-10">
                    ${w.submit.display()|n}
                </div>
            </div>
            '''

        query = twsel.Select2MultipleSelectField(
            name='query',
            label='',
            options=[],
            value='',
            attrs=dict(style='width: 100%;'),
            placeholder=u"Mots clés recherchés...",
            opts=dict(
                tags=[
                    'Python', 'Django', 'Flask', 'Pyramid', 'Turbogears'
                ],
                maximumSelectionSize=10,
                tokenSeparators=[','],
                formatSelectionTooBig=twc.js_callback(
                    """
                    function(a) {
                        return 'Nombre maximum de mots cl\\xE9s atteint.';
                    }
                    """
                )
            ),
            ondemand=True
        )

        center = GeocompleteField(name="center", label="")

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
            name='radius',
            label='',
            options=tmp_options,
            value='',
            attrs=dict(style='width: 100%'),
            placeholder=u'Distance maximale',
            opts=dict(
                allowClear=True,
                formatNoMatches=twc.js_callback(
                    """
                    function() {
                        return 'Aucun r\\xE9sultat ne correpond \\xE0 votre recherche.';
                    }
                    """
                )
            )
        )

        submit = twf.SubmitButton("submit")
        submit.value = "J'effectue ma recherche"
        submit.css_class = "btn btn-default form-control"

    submit = None
