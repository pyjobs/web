<%inherit file="local:templates.master"/>
<%namespace name="admin_helpers" file="local:templates.admin.helpers"/>

<%def name="title()">
    Turbogears Administration System
</%def>

<%def name="page_header()">
    <header class="page-header">
        <h1 class="page-header">Interface de modération de Pyjobs</h1>
    </header>
</%def>

<h3>Modérer des entrées utilisateurs</h3>
<hr>

${admin_helpers.index_list(moderation_list)}

${admin_helpers.link_button(u'/admin', u"Page d'accueil de l'admin", u"Retour à la page d'accueil")}
