# -*- coding: utf-8 -*-
import re

import tw2.core as twc
import tw2.forms as twf
import tw2.forms.widgets as tww
from tw2.core.validation import ValidationError


class PhoneNumberValidator(twc.RegexValidator):
    def __init__(self, **kwargs):
        super(PhoneNumberValidator, self).__init__(**kwargs)

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

    def __init__(self, **kwargs):
        super(SirenValidator, self).__init__(**kwargs)

    def _validate_python(self, value, state=None):
        regex = re.compile('^[0-9]{3}((\-[0-9]{3}){2}|( [0-9]{3}){2})$',
                           re.IGNORECASE)

        # We first check the string format
        if not value or not regex.match(value):
            raise ValidationError('wrong_format', self)

        # The Siren number is formatted correctly, perform the validity check
        value = value.replace('-', '')
        value = value.replace(' ', '')

        digits = [int(x) for x in value]
        digits.reverse()
        validity = 0

        for i, digit in enumerate(digits):
            to_sum = str(digit * 2) if (i + 1) % 2 == 0 else str(digit)

            for figure in to_sum:
                validity += int(figure)

        if validity % 10 != 0:
            raise ValidationError('invalid_siren', self)


class TechnologiesValidator(twc.RegexValidator):
    msgs = {
        'regex': ('badtech', u'Format du champ invalide'),
    }

    def __init__(self, **kwargs):
        super(TechnologiesValidator, self).__init__(**kwargs)

    regex = re.compile('^[^\,,\, , ]+((\,|\, | )[^\,,\, , ]+){0,9}$',
                       re.IGNORECASE | re.UNICODE)


class NewCompanyForm(twf.Form):
    def __init__(self, **kwargs):
        super(NewCompanyForm, self).__init__(**kwargs)
        self.action = '/company/new/submit'
        self.method = 'POST'
        self.submit = None

    class child(tww.BaseLayout):
        inline_engine_name = 'mako'
        template = \
            u'''
            % for c in w.children_hidden:
                ${c.display()}
            % endfor

            <%def name="display_field(field)">
                <div class="form-group required
                ${'has-success' if field.value and not field.error_msg else ''}
                ${'has-error' if field.error_msg else ''}">
                    <label class="control-label col-sm-12" for="${field.compound_id}">${field.label}</label>
                    <div class="col-xs-12 col-sm-12">
                        ${field.display()}
                    </div>
                </div>
                <div class="col-xs-12" style="height:7px;"></div>
            </%def>

            % for child in w.children:
                ${display_field(child)}
            % endfor

            <div class="form-group">
                <label class="control-label col-sm-12" for="submit"> </label>
                <div class="col-xs-12 col-md-12">
                    ${w.submit.display()}
                </div>
            </div>
            '''

        company_name = twf.TextField(
            id='company_name',
            label=u"Nom de l'entreprise:",
            placeholder=u"Mon entreprise qui recrute",
            maxlength=100,
            css_class='form-control',
            validator=twc.Required
        )

        company_siren = twf.TextField(
            id='company_siren',
            label=u"Numéro de Siren:",
            placeholder=u"XXX-XXX-XXX",
            maxlength=11,
            css_class='form-control',
            validator=SirenValidator(required=True)
        )

        company_address = twf.TextField(
            id='company_address',
            label=u"Adresse de l'entreprise:",
            placeholder=u"Adresse l'entreprise",
            maxlength=1024,
            css_class='form-control',
            validator=twc.Required
        )

        company_url = twf.TextField(
            id='company_url',
            label=u"Site web de l'entreprise:",
            placeholder=u"www.pyjobs.fr",
            maxlength=1024,
            css_class='form-control',
            validator=twc.UrlValidator(required=True)
        )

        company_email = twf.TextField(
            id='company_email',
            label=u"Adresse email de contact:",
            placeholder=u"email@exemple.fr",
            maxlength=1024,
            css_class='form-control',
            validator=twc.EmailValidator(required=True)
        )

        company_phone = twf.TextField(
            id='company_phone',
            label=u"Numéro de téléphone:",
            placeholder=u"0X-XX-XX-XX-XX ou +33X-XX-XX-XX-XX ou 0033X-XX-XX-XX-XX",
            maxlength=17,
            css_class='form-control',
            validator=PhoneNumberValidator(required=True)
        )

        company_logo = twf.TextField(
            id='company_logo',
            label=u"Logo de l'entreprise:",
            placeholder=u"http://www.pyjobs.fr/img/pyjobs_logo_square.png",
            maxlength=1024,
            css_class='form-control',
            validator=twc.UrlValidator(required=True)
        )

        company_description = twf.TextArea(
            id='company_description',
            label=u"Description de l'entreprise:",
            placeholder=u"Description de l'entreprise...",
            maxlength=5000,
            css_class='form-control',
            validator=twc.Required
        )

        company_technologies = twf.TextArea(
            name='company_technologies',
            label=u"Technologies utilisées par l'entreprise: (maximum 10)",
            placeholder=u"Technologie 1, Technologie 2, ..., Technologie 10",
            maxlength=200,
            css_class='form-control',
            validator=TechnologiesValidator(required=True)
        )

        submit = twf.SubmitButton('submit')
        submit.value = u"Créer l'entreprise"
        submit.css_class = "btn btn-default form-control"
