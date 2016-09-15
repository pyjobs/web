# -*- coding: utf-8 -*-
import re
import json
from slugify import slugify

import tw2.core as twc
import tw2.forms as twf
import tw2.forms.widgets as tww
from tw2.core.validation import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from pyjobsweb.model import CompanyAlchemy
from pyjobsweb.forms.custom_widgets import GeocompleteField
from pyjobsweb.forms.custom_widgets import PersistentSelect2MultipleSelect

french_validation_messages = {
    'required': u'Veuillez saisir une valeur',
    'decode': u'Mauvais jeu de caractère reçu; devrait être $encoding',
    'corrupt': u"Données du formulaire reçues corrompues; veuillez réessayer "
                u"s'il vous plaît.",
    'childerror': '',  # Children of this widget have errors
}


def _get_technology_list():
    return [
        'Python',
        'Django',
        'Flask',
        'Pyramid',
        'Turbogears',
        'Ansible',
        'Plone',
        'Docker',
        'PostgreSQL',
        'MySQL',
        'Oracle'
    ]


class CompanyNameValidator(twc.Validator):
    def __init__(self, max_length=100, **kwargs):
        super(CompanyNameValidator, self).__init__(**kwargs)
        self.max_length = max_length

        self.msgs = dict(french_validation_messages)
        self.msgs['already_exists'] = u'Cette entreprise existe déjà dans '\
                                      u'notre base'
        self.msgs['toolong'] = u"Nom d'entreprise trop long"

    def _validate_python(self, value, state=None):
        if len(value) > self.max_length:
            raise ValidationError('toolong', self)

        name_slug = slugify(value)

        # Check for duplicates in the database
        try:
            CompanyAlchemy.get_company(name_slug)
        except NoResultFound:
            # There are no duplicates, the validation is therefore successful
            pass
        else:
            # This company slug name is already present in the database, notify
            # the user that the company he's trying to register already exists.
            raise ValidationError('already_exists', self)


class PhoneNumberValidator(twc.RegexValidator):
    def __init__(self, **kwargs):
        super(PhoneNumberValidator, self).__init__(**kwargs)
        self.msgs = dict(french_validation_messages)
        self.msgs['badregex'] = u'Numéro de téléphone invalide'

    regex = re.compile('^0([0-9](\.[0-9]{2}){4})$', re.IGNORECASE)


class SirenValidator(twc.Validator):
    def __init__(self, **kwargs):
        super(SirenValidator, self).__init__(**kwargs)
        self.msgs = dict(french_validation_messages)
        self.msgs['wrong_format'] = (u'Format de saisie non respecté')
        self.msgs['invalid_siren'] = (u'Numéro de Siren invalide')
        self.msgs['duplicate_siren'] = (u'Numéro de Siren déjà utilisé')

    def _validate_python(self, value, state=None):
        regex = re.compile('^[0-9]{3}(( [0-9]{3}){2})$', re.IGNORECASE)

        # We first check the string format
        if not value or not regex.match(value):
            raise ValidationError('wrong_format', self)

        # The Siren number is formatted correctly, perform the validity check
        tmp = value.replace(' ', '')

        digits = [int(x) for x in tmp]
        digits.reverse()
        validity = 0

        for i, digit in enumerate(digits):
            to_sum = str(digit * 2) if (i + 1) % 2 == 0 else str(digit)

            for figure in to_sum:
                validity += int(figure)

        if validity % 10 != 0:
            raise ValidationError('invalid_siren', self)

        # Check for duplicates in the database
        try:
            CompanyAlchemy.get_company(value)
        except NoResultFound:
            # There are no duplicates, the validation is therefore successful
            pass
        else:
            # This Siren number is already present in the database, notify the
            # user that the company he's trying to register already exists.
            raise ValidationError('duplicate_siren', self)


class Select2MultipleSelectValidator(twc.Validator):
    min = 0
    max = 10

    def __init__(self, **kwargs):
        super(Select2MultipleSelectValidator, self).__init__(**kwargs)
        self.msgs = dict(french_validation_messages)
        self.msgs['tooshort'] = u'Soumission trop courte'
        self.msgs['toolong'] = u'Soumission trop longue'

    def _validate_python(self, value, state=None):
        if len(value) > self.max:
            raise ValidationError('toolong', self)
        elif len(value) < self.min:
            raise ValidationError('tooshort', self)


class RequiredValidator(twc.Validator):
    def __init__(self, **kwargs):
        super(RequiredValidator, self).__init__(**kwargs)
        self.msgs = dict(french_validation_messages)
        self.required = True


class LengthValidator(twc.LengthValidator):
    def __init__(self, **kwargs):
        super(LengthValidator, self).__init__(**kwargs)
        self.msgs = dict(french_validation_messages)
        self.msgs['tooshort'] = u'Soumission trop courte'
        self.msgs['toolong'] = u'Soumission trop longue'


class UrlValidator(twc.UrlValidator):
    def __init__(self, **kwargs):
        super(UrlValidator, self).__init__(**kwargs)
        self.msgs = dict(french_validation_messages)
        self.msgs['badregex'] = u'URL invalide'


class EmailValidator(twc.EmailValidator):
    def __init__(self, **kwargs):
        super(EmailValidator, self).__init__(**kwargs)
        self.msgs = dict(french_validation_messages)
        self.msgs['bademail'] = u'Adresse email invalide'


class EmptyHoneyPotValidator(twc.Validator):
    def __init__(self, **kwargs):
        super(EmptyHoneyPotValidator, self).__init__(**kwargs)

    def to_python(self, value, state=None):
        if not self._is_empty(value):
            raise ValidationError('', self)

        return value


class GeocompleteFieldValidator(twc.Validator):
    def __init__(self, **kwargs):
        super(GeocompleteFieldValidator, self).__init__(**kwargs)
        self.msgs = dict(french_validation_messages)
        self.msgs['badformat'] = u'Format invalide'

    def _validate_python(self, value, state=None):
        expected_keys = [
            'name', 'complement', 'country', 'postal_code', 'coordinates']
        sub_keys = {'lat': 'coordinates', 'lon': 'coordinates'}

        try:
            city_dict = json.loads(value)

            for key in expected_keys:
                city_dict[key] = city_dict[key]

            for sub_key, main_key in sub_keys.iteritems():
                city_dict[main_key][sub_key] = city_dict[main_key][sub_key]
        except (Exception, KeyError):
            raise ValidationError('badformat', self)


class NewCompanyForm(twf.Form):
    def __init__(self, **kwargs):
        super(NewCompanyForm, self).__init__(**kwargs)
        self.submit = None
        self.method = 'GET'
        self.attrs = {'enctype': 'application/x-www-form-urlencoded'}
        self.action = '/societes-qui-recrutent/new/submit'

    class child(tww.BaseLayout):
        hover_help = True

        inline_engine_name = 'mako'
        template = \
            u'''
            % for c in w.children_hidden:
                ${c.display()}
            % endfor

            <%def name="display_field(field)">
                <%
                    css_success = ''
                    if field.error_msg:
                        css_success = 'has-error'
                    elif isinstance(field.value, list):
                        if field.value[0]['text']:
                            css_success = 'has-success'
                    elif field.value:
                        css_success = 'has-success'
                %>

                <div class="form-group required ${css_success}"
                title="${field.help_text if field.help_text else ''}">
                    <label class="control-label col-sm-12" for="${field.compound_id}">
                        ${field.label}
                        ${field.error_msg if field.error_msg else ''}
                    </label>
                    <div class="col-xs-12 col-sm-12">
                        ${field.display()}
                    </div>
                </div>
                <div class="col-xs-12" style="height:7px;"></div>
            </%def>

            <%def name="display_honeypot(field)">
                <div class="form-group required honey-field
                ${'has-success' if field.value else ''}"
                title="${field.help_text if field.help_text else ''}">
                    <label class="control-label col-sm-12 honey-field" for="${field.compound_id}">
                        ${field.label}
                        ${field.error_msg if field.error_msg else ''}
                    </label>
                    <div class="col-xs-12 col-sm-12 honey-field">
                        ${field.display()}
                    </div>
                </div>
                <div class="col-xs-12 honey-field" style="height:7px;"></div>
            </%def>

            % for child in w.children_non_hidden:
                % if 'honey-field' in child.css_class:
                    ${display_honeypot(child)}
                % else:
                    ${display_field(child)}
                % endif
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
            help_text=u"Le nom de l'entreprise que vous souhaitez ajouter",
            maxlength=100,
            css_class='form-control',
            validator=CompanyNameValidator(required=True)
        )

        # company_siren = twf.TextField(
        #     id='company_siren',
        #     label=u"Numéro de Siren:",
        #     placeholder=u"XXX XXX XXX",
        #     help_text=u"Le numéro de Siren de l'entreprise que vous souhaitez"
        #               u" ajouter, au format XXX XXX XXX",
        #     maxlength=11,
        #     css_class='form-control',
        #     validator=SirenValidator(required=True)
        # )

        company_street = twf.TextField(
            id='company_street',
            label=u"Rue:",
            placeholder=u"Numéro et nom de rue",
            help_text=u"Numéro et nom de rue",
            maxlength=1024,
            css_class='form-control',
            validator=RequiredValidator
        )

        company_city = GeocompleteField(
            name='company_city',
            label=u'Ville:',
            value='',
            placeholder=u'Nom ville ou CP...',
            attrs=dict(style='width: 100%;'),
            validator=GeocompleteFieldValidator(required=True)
        )

        company_url = twf.TextField(
            id='company_url',
            label=u"Site web de l'entreprise:",
            placeholder=u"http://pyjobs.fr",
            help_text=u"L'url du site web de l'entreprise",
            maxlength=1024,
            css_class='form-control',
            validator=UrlValidator(required=True)
        )

        company_email = twf.TextField(
            id='company_email',
            label=u"Adresse email de contact:",
            placeholder=u"email@exemple.fr",
            help_text=u"L'adresse email de contact de l'entreprise pour les "
                      u"personnes souhaitant candidater",
            maxlength=1024,
            css_class='form-control',
            validator=EmailValidator(required=True)
        )

        company_phone = twf.TextField(
            id='company_phone',
            label=u"Numéro de téléphone:",
            placeholder=u"0X.XX.XX.XX.XX",
            help_text=u"Le numéro de téléphone de contact de l'entreprise pour "
                      u"les personnes souhaitant candidater au format "
                      u"0X.XX.XX.XX.XX",
            maxlength=14,
            css_class='form-control',
            validator=PhoneNumberValidator(required=True)
        )

        company_logo = twf.TextField(
            id='company_logo',
            label=u"Logo de l'entreprise:",
            placeholder=u"http://pyjobs.fr/img/pyjobs_logo_square.png",
            help_text=u"Une url pointant sur une image du logo de l'entreprise",
            maxlength=1024,
            css_class='form-control',
            validator=UrlValidator(required=True)
        )

        company_description = twf.TextArea(
            id='company_description',
            label=u"Description de l'entreprise: (de 100 à 5000 caractères)",
            placeholder=u"Description de l'entreprise...",
            help_text=u"Une description succinte de l'entreprise "
                      u"(de 100 à 5000 caractères)",
            maxlength=5000,
            css_class='form-control',
            validator=LengthValidator(required=True, min=100, max=5000)
        )

        company_technologies = PersistentSelect2MultipleSelect(
            name='company_technologies',
            label=u"Technologies utilisées par l'entreprise: (maximum 10)",
            placeholder=u"Technologie 1, Technologie 2, ..., Technologie 10",
            help_text=u"La liste de technologies utilisées par l'entreprise "
                      u"(max. 10)",
            attrs=dict(style='width: 100%;'),
            opts=dict(
                tags=_get_technology_list(),
                maximumSelectionSize=10,
                tokenSeparators=[',']
            ),
            validator=Select2MultipleSelectValidator(
                required=True, min=1, max=10)
        )

        company_required_field = twf.TextField(
            name='company_required_field',
            label=u'Company label',
            placeholder=u"Label de l'entreprise",
            help_text=u"Message d'aide",
            maxlength=5,
            css_class='form-control honey-field',
            validator=EmptyHoneyPotValidator(required=True)
        )

        submit = twf.SubmitButton('submit')
        submit.value = u"Créer l'entreprise"
        submit.css_class = "btn btn-default form-control"
