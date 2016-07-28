## -*- coding: utf-8 -*-
<%inherit file="local:templates.master"/>

<%def name="head_content()">
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/morris.js/0.5.1/morris.css">
</%def>

<%def name="title()">
    pyjobs — statistiques
</%def>

<%def name="end_body_scripts()">
    <script src="http://code.jquery.com/jquery.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/raphael/2.1.0/raphael-min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/morris.js/0.5.1/morris.min.js"></script>
    <script>
        $(document).ready(function () {
            Morris.Line({
                element: 'month_chart',
                data: ${h.to_json(flat_month, indent=4) | n},
                xkey: ${h.to_json(flat_x_field) | n},
                ykeys: ${h.to_json(flat_y_fields) | n},
                labels: ${h.to_json(sources_labels) | n}
            });

            Morris.Line({
                element: 'weeks_chart',
                data: ${h.to_json(flat_week, indent=4) | n},
                xkey: ${h.to_json(flat_x_field) | n},
                ykeys: ${h.to_json(flat_y_fields) | n},
                labels: ${h.to_json(sources_labels) | n}
            });
        });
    </script>
</%def>

<%def name="stats_table(stats, periods, period_format)">
    <table class="stats table table-striped table-hover">
        <thead>
        <th>
            Source
        </th>
            % for period in periods:
                <th>
                    ${period.strftime(period_format)}
                </th>
            % endfor
        </thead>
        <tbody>
            % for source in stats:
                <tr>
                    <td>
                        ${sources[source].label}
                    </td>
                    % for period in periods:
                        <td>
                            ${stats[source][period]}
                        </td>
                    % endfor
                </tr>
            % endfor
        </tbody>
    </table>
</%def>

<%def name="page_header()">
    <header class="page-header">
        <h1>Statistiques</h1>
    </header>
</%def>

<h2>Publication d'offres par mois</h2>

${stats_table(stats=stats_month, periods=months, period_format="%B %Y")}

<div id="month_chart" style="height: 250px;"></div>

<h2>Publication d'offres par semaines</h2>

${stats_table(stats=stats_week, periods=weeks, period_format="%Y, semaine %W")}

<div id="weeks_chart" style="height: 250px;"></div>
