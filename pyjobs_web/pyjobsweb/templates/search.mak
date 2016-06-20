## -*- coding: utf-8 -*-
<%inherit file="local:templates.master"/>

<%def name="title()">
    pyjobs — rechercher un job
</%def>

<h1>Effectuer une recherche d'emploi</h1>

<div id="research_form">
    ${form.display()|n}
</div>
