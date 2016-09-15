<%inherit file="local:templates.master"/>
<%namespace name="admin_helpers" file="local:templates.admin.helpers"/>

<%def name="title()">
    Turbogears Administration System
</%def>

<%def name="page_header()">
    <header class="page-header">
        <h1 class="page-header">Interface d'administration de Pyjobs</h1>
    </header>
</%def>

<a href="moderation"><h3>Interface de modération</h3></a>
<hr>

${admin_helpers.index_list(moderation_list)}

<a href="geocoding"><h3>Résoudre les problèmes de géocoding</h3></a>
<hr>

${admin_helpers.index_list(geocoding_list)}

<h3>Administrer la base de données Postgresql</h3>
<hr>

${admin_helpers.index_list(model_list)}

${admin_helpers.link_button(u'/', u"Retour page d'accueil du site", u'Retour au site')}
