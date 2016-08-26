<%inherit file="local:templates.master"/>

<%def name="title()">
    ${tmpl_context.title} - ${model}
</%def>

<div class="row">
    <div class="col-md-2">
        % if hasattr(tmpl_context, 'menu_items'):
            <ul class="nav crud-sidebar hidden-xs hidden-sm">
                % for lower, item in sorted(tmpl_context.menu_items.items()):
                    <li class="${item==model and 'active' or ''}">
                        <a href="${tmpl_context.crud_helpers.make_link(lower, pk_count or 1)}">${item}</a>
                    </li>
                % endfor
            </ul>
        % endif
    </div>

    <div class="col-md-10">
        <h1 class="page-header">Modération - ${model}</h1>
        ${tmpl_context.widget(value=value, action='./') | n}

        <br/>

        <form method="POST" action="${delete_url}">
            <input name="_method" value="DELETE" type="hidden">
            <button type="submit" class="btn btn-danger" onclick="return confirm('Êtes-vous sûr ? Cette opération est irréversible.')">
                Rejeter
            </button>
        </form>

        <br/>

        <a href="/admin/moderation/${model.lower()}s" title="Liste des ${model}" class="btn btn-default">
            Retour à la liste des ${model}
        </a>
    </div>
</div>