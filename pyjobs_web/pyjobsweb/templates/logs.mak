## -*- coding: utf-8 -*-
<%inherit file="local:templates.master"/>

<%def name="title()">
    PyJobs: LOGS
</%def>

<%def name="html_class()">full-height</%def>
<%def name="body_class()">full-height</%def>
<%def name="container_class()">full-height</%def>

<caption>Last ${last_days} day(s) LOGS (source=xxx&last_days=x for filter)</caption>

<div class="full-page-container">

</div>
<textarea class="full-page">
    % for log in logs:
${log.datetime} ${log.source} ${log.message}
    % endfor
</textarea>
