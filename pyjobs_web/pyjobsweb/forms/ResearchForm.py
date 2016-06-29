# -*- coding: utf-8 -*-
import tw2.core as twc
import tw2.forms as twf


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

        query = twf.TextField(name="query", label="")
        query.css_class = "form-control"
        query.placeholder = u"Mot clés recherchés..."
        query.value = ""

        center = twf.TextField(name="center", label="")
        center.css_class = "form-control"
        center.placeholder = u"Géolocalisation..."
        center.value = ""

        radius = twf.SingleSelectField(name="radius", label="")
        radius.css_class = "form-control col-sm-12"
        distances = [
            "5", "10", "25", "50", "100", "200", "200+"
        ]
        options = []
        for i, d in enumerate(distances):
            distances_km = "{}{}".format(d, "km")
            if i == len(distances) - 1:
                option = ('infty', distances_km)
            else:
                option = (d, distances_km)

            options.append(option)

        radius.options = options
        radius.prompt_text = "Distance maximale"

        unit = twf.HiddenField(name="unit", label="", value="km")

        submit = twf.SubmitButton("submit")
        submit.value = "J'effectue ma recherche"
        submit.css_class = "btn btn-default form-control"

    submit = None
