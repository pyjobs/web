# -*- coding: utf-8 -*-
import tw2.core as twc
import tw2.jqplugins.select2 as twsel
from tw2.core.validation import Validator


class GeocompleteField(twsel.Select2AjaxSingleSelectField):
    def __init__(self, **kwargs):
        super(GeocompleteField, self).__init__(**kwargs)

    attrs = dict(style='width: 100%;')
    options = []
    validator = Validator()
    opts = dict(
        placeholder=u'Autour de...',
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
