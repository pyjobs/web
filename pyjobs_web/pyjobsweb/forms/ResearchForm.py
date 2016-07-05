# -*- coding: utf-8 -*-
import tw2.core as twc
import tw2.forms as twf
import tw2.jqplugins.select2 as twsel


class GeocompleteField(twsel.Select2AjaxSingleSelectField):
    attrs = dict(style='width: 100%;')
    options = []
    opts = dict(
        placeholder=u'Rechercher une localisation...',
        no_results_text=u'Aucun résultat ne correspond à votre recherche...',
        minimumInputLength=1,
        ajax=dict(
            # instead of writing the function to execute the
            # request we use Select2's convenient helper
            url="TODO",
            dataType='TODO',
            delay=100,
            data=twc.js_callback(
                """
                function (term, page) {
                    // TODO
                }
                """
            ),
            results=twc.js_callback(
                """
                function (data, page) {
                    // TODO
                }
                """
            ),
        ),
        initSelection=twc.js_callback(
            """
            function(element, callback) {
                // TODO
            }
            """
        ),
        formatSelection=twc.js_callback(
            """
            function(movie) {
                // TODO
            }
            """
        ),
        formatResult=twc.js_callback(
            """
            function(movie) {
                // TODO
            }
            """
        ),
        formatInputTooShort=twc.js_callback(
            """
            function() {
                return 'Veuillez saisir %s caract\\xE8re(s) suppl\\xE9mentaire(s)...';
            }
            """ % 1
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
                tokenSeparators=[",", " "]
            ),
            ondemand=True,
        )

        center = GeocompleteField(name="center", label="")

        radius = twsel.Select2SingleSelectField(name="radius", label="")
        radius.attrs = dict(style='width: 100%')
        radius.css_class = "col-sm-12"
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

        radius.options = tmp_options
        radius.placeholder = u'Distance maximale'

        unit = twf.HiddenField(name="unit", label="", value="km")

        submit = twf.SubmitButton("submit")
        submit.value = "J'effectue ma recherche"
        submit.css_class = "btn btn-default form-control"

    submit = None
