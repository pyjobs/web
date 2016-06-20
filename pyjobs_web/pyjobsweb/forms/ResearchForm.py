# -*- coding: utf-8 -*-
import tw2.core as twc
import tw2.forms as twf


class ResearchForm(twf.Form):
    class child(twf.TableLayout):
        keywords = twf.TextField(
            "keywords", label=u"Mots clés : ", validator=twc.Required
        )
        keywords.css_class = "form-control"
        keywords.placeholder = u"Mot clés recherchés..."
        keywords.value = ""
        keywords.name = "keywords"

    submit = twf.SubmitButton("submit")
    submit.value = "J'effectue ma recherche !"
    submit.css_class = "btn btn-default right"
