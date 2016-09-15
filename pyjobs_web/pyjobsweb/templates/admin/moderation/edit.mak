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
        <h1 class="page-header">Modération - ${model}</h1>

        ${admin_helpers.address_validation_button()}

        ${tmpl_context.widget(value=value, action='./')}

        <br/>

        ${admin_helpers.delete_button(delete_url, u'Rejeter', u'Êtes-vous sûr ? Cette opération est irréversible.')}

        <br/>

        ${admin_helpers.link_button(u'/admin/moderation/%ss' % model.lower(), u'Liste des %ss' % model, u'Retour à la liste des %ss' % model)}
    </div>
</div>