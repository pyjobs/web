# -*- coding: utf-8 -*-
import tw2.core as twc
import tw2.forms as twf
import tw2.jqplugins.select2 as twsel
import tg


class GeocompleteField(twsel.Select2AjaxSingleSelectField):
    attrs = dict(style='width: 100%;')
    options = []
    opts = dict(
        placeholder=u'Rechercher une localisation...',
        minimumInputLength=1,
        maximumInputLength=125,
        allowClear=True,
        ajax=dict(
            # url='{}/geocomplete'.format(
            #     tg.config.get('site.domain_base_url')
            # ),
            url='/geocomplete',
            dataType='json',
            type='POST',
            delay=250,
            cache=True,
            data=twc.js_callback(
                """
                function (term, page) {
                    return {address: term};
                }
                """
            ),
            results=twc.js_callback(
                """
                function (data, page) {
                    var results = [];
                    $.each(data['results'], function (i, v) {
                        var o = {};
                        o.id = v;
                        o.name = v;
                        o.value = v;
                        results.push(o);
                    })

                    return {
                        results: results
                    };
                }
                """
            ),
        ),
        espaceMarkup=twc.js_callback(
            """
            function(markup) {
                return markup;
            }
            """
        ),
        formatResult=twc.js_callback(
            """
            function(location) {
                var markup = '<option value="' + location.value + '">' + location.name + '</option>';
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
            function() {
                return 'Veuillez saisir %s caract\\xE8re(s) suppl\\xE9mentaire(s).';
            }
            """ % 1
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
            <div class="container">
                <h2>Rechercher une offre d'emploi</h2>
                <form class="form-horizontal" role="form">
                    <div class="form-group">
                        <label class="control-label col-sm-2" for="query">Requête :</label>
                        <div class="col-sm-10">
                            ${w.children.query.display()|n}
                        </div>
                    </div>
                    <div class="col-xs-12" style="height:3px;"></div>
                    <div class="form-group">
                        <label class="control-label col-sm-2" for="from_location">Autour de :</label>
                        <div class="col-sm-10">
                            ${w.children.center.display()|n}
                        </div>
                    </div>
                    <div class="col-xs-12" style="height:3px;"></div>
                    <div class="form-group">
                        <label class="control-label col-sm-2" for="max_dist">Dans un rayon de :</label>
                        <div class="col-sm-10">
                            ${w.children.radius.display()|n}
                        </div>
                    </div>
                    <div class="col-xs-12" style="height:3px;"></div>
                    <div class="form-group">
                        <div class="col-sm-offset-2 col-md-10">
                            ${w.submit.display()|n}
                        </div>
                    </div>
                    ${w.children.unit.display()|n}
                </form>
            </div>
            '''

        query = twsel.Select2MultipleSelectField(
            name='query',
            label='',
            options=[],
            value='',
            attrs=dict(style='width: 100%;'),
            placeholder=u"Mot clés recherchés...",
            opts=dict(
                tags=['Python', 'Django', 'Turbogears', 'Pypi'],
                maximumSelectionSize=10,
                tokenSeparators=[",", " "],
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
            opts=dict(allowClear=True)
        )

        unit = twf.HiddenField(name="unit", label="", value="km")

        submit = twf.SubmitButton("submit")
        submit.value = "J'effectue ma recherche"
        submit.css_class = "btn btn-default form-control"

    submit = None
