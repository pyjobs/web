# -*- coding: utf-8 -*-
import tw2.core as twc
import tw2.forms as twf


class ResearchForm(twf.Form):
    class child(twf.TableLayout):
        keywords = twf.TextField(
            "keywords", label="", validator=twc.Required
        )
        keywords.css_class = "form-control"
        keywords.placeholder = u"Mot clés recherchés..."
        keywords.value = ""
        keywords.name = "keywords"

        geoloc = twf.TextField(
            "geoloc", label="", validator=twc.Required
        )
        geoloc.css_class = "form-control"
        geoloc.placeholder = u"Géolocalisation..."
        geoloc.value = ""
        geoloc.name = "geoloc"

    submit = twf.SubmitButton("submit")
    submit.value = "Go !"
    submit.css_class = "btn btn-default right"
