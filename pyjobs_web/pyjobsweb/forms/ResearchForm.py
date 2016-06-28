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
                            ${w.children.from_location.display()|n}
                        </div>
                    </div>
                    <div class="col-xs-12" style="height:3px;"></div>
                    <div class="form-group">
                        <label class="control-label col-sm-2" for="max_dist">Dans un rayon de :</label>
                        <div class="col-sm-10">
                            ${w.children.max_dist.display()|n}
                        </div>
                    </div>
                    <div class="col-xs-12" style="height:3px;"></div>
                    <div class="form-group">
                        <div class="col-sm-offset-2 col-md-10">
                            ${w.submit.display()|n}
                        </div>
                    </div>
                </form>
            </div>
            '''

        query = twf.TextField(
                name="query", label=""
        )
        query.css_class = "form-control"
        query.placeholder = u"Mot clés recherchés..."
        query.value = ""

        from_location = twf.TextField(
                name="from_location", label=""
        )
        from_location.css_class = "form-control"
        from_location.placeholder = u"Géolocalisation..."
        from_location.value = ""

        max_dist = twf.SingleSelectField(
                name="max_dist", label=""
        )
        max_dist.css_class = "form-control col-sm-12"
        distances = [
            "5", "10", "25", "50", "100", "200", "200+"
        ]
        distances_km = []
        for d in distances:
            distances_km.append("{}{}".format(d, "km"))
        max_dist.options = distances_km
        max_dist.prompt_text = "Distance maximale"

        submit = twf.SubmitButton("submit")
        submit.value = "J'effectue ma recherche"
        submit.css_class = "btn btn-default form-control"

    submit = None
