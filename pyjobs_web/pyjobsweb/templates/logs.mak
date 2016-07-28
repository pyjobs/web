## -*- coding: utf-8 -*-
<%inherit file="local:templates.master"/>

<%def name="title()">
    pyjobs — logs de crawling
</%def>

<%def name="html_class()">full-height</%def>
<%def name="body_class()">full-height</%def>
<%def name="container_class()">full-height</%def>

<%def name="page_header()">
    <header class="page-header">
        <h1>Crawling logs</h1>
    </header>
</%def>

<caption>Last ${last_days} day(s) LOGS (source=xxx&last_days=x for filter)</caption>

<textarea class="logs-text-area form-control" readonly>
    % for log in logs:
        ${log.datetime} ${log.source} ${log.message}
    % endfor
</textarea>
