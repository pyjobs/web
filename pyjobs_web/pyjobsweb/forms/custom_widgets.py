# -*- coding: utf-8 -*-
import tw2.core as twc
import tw2.jqplugins.select2 as twsel


class GeocompleteField(twsel.Select2AjaxSingleSelectField):
    def __init__(self, **kwargs):
        super(GeocompleteField, self).__init__(**kwargs)

    attrs = dict(style='width: 100%;')
    options = []
    opts = dict(
        placeholder=u'Autour de...',
        minimumInputLength=1,
        maximumInputLength=125,
        allowClear=True,
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
                            o.id = v['to_submit'];
                            o.name = v['to_display'];
                            o.value = v['to_display'];
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
                return location.value || location.text
            }
            """
        )
    )
