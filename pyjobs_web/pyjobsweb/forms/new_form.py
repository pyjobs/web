# -*- coding: utf-8 -*-
import re

import tw2.core as twc
import tw2.forms as twf
import tw2.forms.widgets as tww
import tw2.jqplugins.select2 as twsel
from tw2.core.validation import ValidationError


class PhoneNumberValidator(twc.RegexValidator):
    def __init__(self, required=False, **kwargs):
        super(PhoneNumberValidator, self).__init__(**kwargs)
        self.required = required

    msgs = {
        'regex': ('badphone', u'Numéro de téléphone invalide'),
    }

    regex = re.compile('^(0|\+33|0033)'
                       '([0-9](\-[0-9]{2}){4}'
                       '|[0-9](\.[0-9]{2}){4}'
                       '|[0-9]( [0-9]{2}){4}'
                       '|[0-9]{9})$',
                       re.IGNORECASE)


class SirenValidator(twc.Validator):
    msg = {
        'wrong_format': u'Format de saisie non respecté',
        'invalid_siren': u'Numéro de Siren invalide',
    }

    def __init__(self, required=False, **kwargs):
        super(SirenValidator, self).__init__(**kwargs)
        self.required = required

    def _validate_python(self, value, state=None):
        regex = re.compile('^[0-9]{3}(\-[0-9]{3}){2}$', re.IGNORECASE)

        # We first check the string format
        if not value or not value[1] or not regex.match(value[1]):
            raise ValidationError('wrong_format', self)

        # The Siren number is formatted correctly, perform the validity check
        digits = [int(x) for x in value[1].replace('-', '')]
        validity = 0

        for i, digit in enumerate(digits):
            validity += digit * 2 if (i + 1) % 2 == 0 else digit

        if validity % 10 != 0:
            raise ValidationError('invalid_siren', self)


class NewCompanyForm(twf.Form):
    def __init__(self, **kwargs):
        super(NewCompanyForm, self).__init__(**kwargs)
        self.submit = None

    class child(tww.BaseLayout):
        inline_engine_name = 'mako'
        template = \
            u'''
            <div class="form-group">
                <label class="control-label col-sm-12" for="company_name">Nom de l'entreprise:</label>
                <div class="col-xs-12 col-sm-12">
                    ${w.children.company_name.display()|n}
                </div>
            </div>
            <div class="col-xs-12" style="height:3px;"></div>
            <div class="form-group">
                <label class="control-label col-sm-12" for="company_siren">Numéro de Siren:</label>
                <div class="col-xs-12 col-sm-12">
                    ${w.children.company_siren.display()|n}
                </div>
            </div>
            <div class="col-xs-12" style="height:3px;"></div>
            <div class="form-group">
                <label class="control-label col-sm-12" for="company_address">Adresse de l'entreprise:</label>
                <div class="col-xs-12 col-sm-12">
                    ${w.children.company_address.display()|n}
                </div>
            </div>
            <div class="col-xs-12" style="height:3px;"></div>
            <div class="form-group">
                <label class="control-label col-sm-12" for="company_url">Site web de l'entreprise:</label>
                <div class="col-xs-12 col-sm-12">
                    ${w.children.company_url.display()|n}
                </div>
            </div>
            <div class="col-xs-12" style="height:3px;"></div>
            <div class="form-group">
                <label class="control-label col-sm-12" for="company_email">Adresse email de contact:</label>
                <div class="col-xs-12 col-sm-12">
                    ${w.children.company_email.display()|n}
                </div>
            </div>
            <div class="col-xs-12" style="height:3px;"></div>
            <div class="form-group">
                <label class="control-label col-sm-12" for="company_phone">Numéro de téléphone:</label>
                <div class="col-xs-12 col-sm-12">
                    ${w.children.company_phone.display()|n}
                </div>
            </div>
            <div class="col-xs-12" style="height:3px;"></div>
            <div class="form-group">
                <label class="control-label col-sm-12" for="company_siren">Numéro de Siren:</label>
                <div class="col-xs-12 col-sm-12">
                    ${w.children.company_siren.display()|n}
                </div>
            </div>
            <div class="col-xs-12" style="height:3px;"></div>
            <div class="form-group">
                <label class="control-label col-sm-12" for="company_logo">Logo de l'entreprise:</label>
                <div class="col-xs-12 col-sm-12">
                    ${w.children.company_logo.display()|n}
                </div>
            </div>
            <div class="col-xs-12" style="height:3px;"></div>
            <div class="form-group">
                <label class="control-label col-sm-12" for="company_description">Description de l'entreprise:</label>
                <div class="col-xs-12 col-sm-12">
                    ${w.children.company_description.display()|n}
                </div>
            </div>
            <div class="col-xs-12" style="height:3px;"></div>
            <div class="form-group">
                <label class="control-label col-sm-12" for="company_technologies">Technologies utilisées par l'entreprise:</label>
                <div class="col-xs-12 col-sm-12">
                    ${w.children.company_technologies.display()|n}
                </div>
            </div>
            <div class="col-xs-12" style="height:3px;"></div>
            <div class="form-group">
                <label class="control-label col-sm-12" for="submit"> </label>
                <div class="col-xs-12 col-md-12">
                    ${w.submit.display()|n}
                </div>
            </div>
            '''

        company_name = twf.TextField(id='company_name',
                                     placeholder=u"Mon entreprise qui recrute",
                                     maxlength=100,
                                     css_class='form-control',
                                     validator=twc.Required)

        company_siren = twf.TextField(id='company_siren',
                                      placeholder=u"XXX-XXX-XXX",
                                      maxlength=11,
                                      css_class='form-control',
                                      validator=SirenValidator)

        company_address = twf.TextField(id='company_address',
                                        placeholder=u"Adresse l'entreprise",
                                        maxlength=1024,
                                        css_class='form-control',
                                        validator=twc.Required)

        company_url = twf.TextField(id='company_url',
                                    placeholder=u"www.pyjobs.fr",
                                    maxlength=1024,
                                    css_class='form-control',
                                    validator=twc.UrlValidator)

        company_email = twf.TextField(id='company_email',
                                      placeholder=u"email@exemple.fr",
                                      maxlength=1024,
                                      css_class='form-control',
                                      validator=twc.EmailValidator)

        company_phone = twf.TextField(id='company_phone',
                                      placeholder=u"XX-XX-XX-XX-XX ou +33X-XX-XX-XX-XX ou 0033X-XX-XX-XX-XX",
                                      maxlength=17,
                                      css_class='form-control',
                                      validator=PhoneNumberValidator)

        company_logo = twf.TextField(id='company_logo',
                                     placeholder=u"www.pyjobs.fr/img/pyjobs_logo_square.png",
                                     maxlength=1024,
                                     css_class='form-control',
                                     validator=twc.UrlValidator)

        company_description = twf.TextArea(id='company_description',
                                           placeholder=u"Description de l'entreprise...",
                                           maxlength=5000,
                                           css_class='form-control',
                                           validator=twc.Required)

        company_technologies = twsel.Select2MultipleSelectField(
            name='technologies',
            label='',
            options=[],
            value='',
            attrs=dict(style='width: 100%;'),
            placeholder=u"Technologies utilisées...",
            opts=dict(
                tags=[
                    'Python', 'Django', 'Flask', 'Pyramid', 'Turbogears'
                ],
                minimumSelectionSize=1,
                maximumSelectionSize=10,
                tokenSeparators=[','],
                formatSelectionTooBig=twc.js_callback(
                    """
                    function(a) {
                        return 'Nombre maximum de technologies atteint.';
                    }
                    """
                )
            ),
            ondemand=True,
            css_class='form-control'
        )

        submit = twf.SubmitButton('submit')
        submit.value = u"Créer l'entreprise"
        submit.css_class = "btn btn-default form-control"
