<%inherit file="local:templates.master"/>

<%def name="title()">
    Turbogears Administration System
</%def>

<%def name="page_header()">
    <header class="page-header">
        <h1 class="page-header">Interface d'administration de Pyjobs</h1>
    </header>
</%def>

<%def name="admin_index_list(list_elements)">
    <div class="row">
        <div class="col-md-12">
            <div class="list-group">
                % for elem in list_elements:
                    <a class="list-group-item" href="${elem['link']}">
                        <h4 class="list-group-item-heading">
                            <span class="glyphicon glyphicon-list-alt"></span> ${elem['display']}
                        </h4>
                    </a>
                % endfor
            </div>
        </div>
    </div>
</%def>

<h3>Administrer la base de données Postgresql:</h3>
<hr>

${admin_index_list(model_list)}

<a href="geocoding"><h3>Résoudre les problèmes de géocoding:</h3></a>
<hr>

${admin_index_list(geocoding_list)}

<a href="moderation"><h3>Modérer des entreprises:</h3></a>
<hr>

${admin_index_list(moderation_list)}

<a href="/" title="Page d'acceuil de l'admin" class="btn btn-default">
    Retour au site
</a>
