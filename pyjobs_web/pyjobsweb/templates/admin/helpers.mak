<%def name="address_validation_scripts(address_field_id)">
    <script type="text/javascript">
        $(document).ready(function () {
            $("#address-validation").click(function () {
                var address = $("#${address_field_id}").val();
                var nominatim = "https://www.openstreetmap.org/search?query=";
                window.open(nominatim.concat(address), '_blank');
            });
        });
    </script>
</%def>

<%def name="address_validation_button()">
    <div class="form-group">
        <button id="address-validation" type="button" class="btn btn-info">
            Vérifier la validité de l'adresse
        </button>
    </div>
</%def>

<%def name="delete_button(action, text, confirm_text)">
    <form method="POST" action="${action}">
        <input name="_method" value="DELETE" type="hidden">
        <button type="submit" class="btn btn-danger" onclick="return confirm(${confirm_text})">
            ${text}
        </button>
    </form>
</%def>

<%def name="link_button(url, title, text)">
    <a href="${url}" title="${title}" class="btn btn-default">
        ${text}
    </a>
</%def>

<%def name="side_list()">
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
</%def>

<%def name="index_list(list_elements)">
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
