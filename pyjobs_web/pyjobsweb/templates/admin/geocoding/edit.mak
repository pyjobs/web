<%inherit file="local:templates.master"/>
<%namespace name="admin_helpers" file="local:templates.admin.helpers"/>

<%def name="title()">
    ${tmpl_context.title} - ${model}
</%def>

<%def name="end_body_scripts()">
    ${parent.end_body_scripts()}
    ${admin_helpers.address_validation_scripts('sx_address')}
</%def>

<div class="row">
    ${admin_helpers.side_list()}

    <div class="col-md-10">
        <h1 class="page-header">Résoudre les problèmes de géocoding - ${model}</h1>

        ${admin_helpers.address_validation_button() | n}

        ${tmpl_context.widget(value=value, action='./') | n}

        <br/>

        ${admin_helpers.link_button(u'/admin/geocoding/%ss' % model.lower(), u'Liste des %ss' % model, u'Retour à la liste des %ss' % model)}
    </div>
</div>