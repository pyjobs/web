<%inherit file="local:templates.master"/>
<%namespace name="admin_helpers" file="local:templates.admin.helpers"/>

<%def name="title()">
    ${tmpl_context.title} - ${model}
</%def>

<div class="row">
    ${admin_helpers.side_list()}

    <div class="col-md-10">
        <h1 class="page-header">Edit ${model}</h1>
        ${tmpl_context.widget(value=value, action='./') | n}

        <br/>

        ${admin_helpers.link_button(u'/admin/%ss' % model.lower(), u'Liste des %ss' % model, u'Retour à la liste des %ss' % model)}
    </div>
</div>