## -*- coding: utf-8 -*-
<%inherit file="local:templates.master"/>

##     <link rel="stylesheet" href="//cdn.jsdelivr.net/chartist.js/latest/chartist.min.css">
##     <script src="//cdn.jsdelivr.net/chartist.js/latest/chartist.min.js"></script>
##
## <div class="ct-chart"></div>
##
## <script>
##     var data = {
##       // A labels array that can contain any sort of values
##       labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
##       // Our series array that contains series objects or in this case series data arrays
##       series: [
##         [5, 2, 4, 2, 0]
##       ]
##     };
##
##     // As options we currently only set a static size of 300x200 px. We can also omit this and use aspect ratio containers
##     // as you saw in the previous example
##     var options = {
##       width: 600,
##       height: 400
##     };
##
##     options = {}
##
##     // Create a new line chart object where as first parameter we pass in a selector
##     // that is resolving to our chart container element. The Second parameter
##     // is the actual data object. As a third parameter we pass in our custom options.
##     new Chartist.Bar('.ct-chart', data, options);
## </script>

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
