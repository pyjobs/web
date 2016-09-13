# -*- coding: utf-8 -*-
import tw2.core as twc
import tw2.jqplugins.select2 as twsel
from tw2.core.validation import Validator


class PersistentSelect2MultipleSelect(twsel.Select2MultipleSelectField):
    def __init__(self, **kwargs):
        super(PersistentSelect2MultipleSelect, self).__init__(**kwargs)
        self.resources = []
        self.ondemand = True
        self.validator = Validator()

        options = self.options
        self.options = []

        self.opts = dict()
        self.opts['tags'] = options
        self.opts['maximumSelectionSize'] = 10
        self.opts['tokenSeparators'] = [',']
        self.opts['initSelection'] = twc.js_callback(
            '''
            function(element, callback) {
                var init_data = [];

                param = params['%(param)s'];

                if(typeof param !== "undefined" && param) {
                    $.each(param.split(','), function(i, v) {
                        var elem = {};
                        elem.id = v;
                        elem.text = v;
                        init_data.push(elem);
                    });
                }

                callback(init_data);
            }
            ''' % dict(param=self.name)
        )


class PersistentSelect2SingleSelect(twsel.Select2SingleSelectField):
    def __init__(self, **kwargs):
        super(PersistentSelect2SingleSelect, self).__init__(**kwargs)
        self.resources = []

        self.ondemand = True,
        self.validator = Validator()

        self.js_dict_entries = ['%s: "%s"' % (key, value)
                                for key, value in self.options]
        self.js_opts_dict = '{%s}' % ', '.join(self.js_dict_entries)

        self.opts = dict()
        self.opts['allowClear'] = True
        self.opts['initSelection'] = twc.js_callback(
            '''
            function (element, callback) {
                var init_data;
                var list_opts = %(options)s;
                var param = params['%(param)s'];

                if(typeof param !== "undefined" && param) {
                    var elem = {};
                    elem.id = param;

                    if(param in list_opts) {
                        elem.text = list_opts[param];
                    }

                    init_data = elem;
                }

                callback(init_data);
            }
            ''' % dict(options=self.js_opts_dict, param=self.name)
        )


class GeocompleteField(twsel.Select2AjaxSingleSelectField):
    def __init__(self, **kwargs):
        super(GeocompleteField, self).__init__(**kwargs)
        self.resources = [
            twc.JSSource(
                src='''
                function format_name(name, complement, postal_code, country) {
                    var display_name = name;
                    display_name += ' ';

                    if(complement) {
                        display_name += complement;
                    }

                    display_name += ' - ';
                    display_name += postal_code;
                    display_name += ', ';
                    display_name += country;

                    return display_name.toUpperCase();
                }
                '''
            )
        ]
        self.options = []
        self.ondemand = True
        self.validator = Validator()

    opts = dict(
        minimumInputLength=1,
        maximumInputLength=125,
        allowClear=True,
        dropdownAutoWidth=True,
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
                            o.id = JSON.stringify(v);
                            o.name = format_name(v['name'], v['complement'], v['postal_code'], v['country']);
                            o.value = format_name(v['name'], v['complement'], v['postal_code'], v['country']);
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
        initSelection=twc.js_callback(
            """
            function (element, callback) {
                var init_data;

                center = params['center'];

                if(typeof center !== "undefined" && center) {
                    var elem = {};
                    center_dict = JSON.parse(center);
                    elem.id = center;
                    elem.name = format_name(center_dict['name'], center_dict['complement'], center_dict['postal_code'], center_dict['country']);
                    elem.value = format_name(center_dict['name'], center_dict['complement'], center_dict['postal_code'], center_dict['country']);
                    init_data = elem;
                }

                callback(init_data);
            }
            """
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
                if(typeof location !== "undefined") {
                    return location.value || location.text;
                }
            }
            """
        )
    )
