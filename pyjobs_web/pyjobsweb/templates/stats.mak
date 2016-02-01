## -*- coding: utf-8 -*-
<%inherit file="local:templates.master"/>

<%def name="stats_table(stats, periods, period_format)">
    <table class="stats table">
        <thead>
        <th>
            % for period in periods:

                <th>
                    ${period.strftime(period_format)}
                </th>
            % endfor
        </th>
        </thead>
        <tbody>
            % for source in stats:
                <tr>
                    <td>
                        ${source}
                    </td>
                    % for date in stats[source]:
                        <td>
                            ${stats[source][date]}
                        </td>
                    % endfor
                </tr>
            % endfor
        </tbody>
    </table>
</%def>

<h1>Statistiques</h1>

<h2>Publication d'offres par mois</h2>

${stats_table(stats=stats_month, periods=months, period_format="%B %Y")}

<h2>Publication d'offres par semaines</h2>

${stats_table(stats=stats_week, periods=weeks, period_format="%Y %W")}





<script>

</script>
