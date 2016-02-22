## -*- coding: utf-8 -*-
<%inherit file="local:templates.master"/>

<%def name="title()">
    PyJobs: LOGS
</%def>


<table class="table">
    <caption>Last 24 hours LOGS (source=xxx&last_days=x for filter)</caption>
    <thead>
    <tr>
        <th>Date</th>
        <th>Source</th>
        <th>Message</th>
    </tr>
    </thead>
    <tbody>

    % for log in logs:
        <tr>
            <th scope="row">${log.datetime}</th>
            <td>${log.source}</td>
            <td>${log.message}</td>
        </tr>
    % endfor

    </tbody>
</table>