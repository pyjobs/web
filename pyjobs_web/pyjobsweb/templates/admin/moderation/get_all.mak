<%inherit file="local:templates.master"/>
<%namespace name="admin_helpers" file="local:templates.admin.helpers"/>

<%def name="title()">
    ${tmpl_context.title} - ${model} Listing
</%def>

<%
    PAGER_ARGS = tmpl_context.make_pager_args(link=mount_point+'/',
                                          page_link_template='<li><a%s>%s</a></li>',
                                          page_plain_template='<li%s><span>%s</span></li>',
                                          curpage_attr={'class': 'active'})
%>

<div class="row">
    ${admin_helpers.side_list()}

    <div class="col-md-10">
        <h1 class="page-header">Liste des "${model}" en attente de modération</h1>

        <div class="row">
            <div class="col-xs-9 col-md-5">
                % if tmpl_context.paginators:
                    <ul class="pagination pull-sm-right" style="margin:0;">
                        ${tmpl_context.paginators.value_list.pager(**PAGER_ARGS)}
                    </ul>
                % endif
            </div>

            <div class="col-xs-12 col-md-7">
                <div class="hidden-lg hidden-md">&nbsp;</div>
                % if search_fields:
                    <form class="form-inline pull-md-right">
                        <div class="form-group">
                            <select id="crud_search_field" class="form-control"
                                    onchange="crud_search_field_changed(this);">
                                % for field, name, selected in search_fields:
                                    % if selected is not False:
                                        <option value="${field}"
                                                selected="selected">${name}</option>
                                    % else:
                                        <option value="${field}">${name}</option>
                                    % endif
                                % endfor
                            </select>
                        </div>

                        <div class="form-group">
                            <input id="crud_search_value" class="form-control"
                                   type="text"
                                   placeholder="equals / contains"
                                   name="${current_search[0]}"
                                   value="${current_search[1]}"/>
                        </div>

                        <button type="submit" class="btn btn-default">Search
                        </button>
                    </form>
                % endif
            </div>
        </div>


        <br/>

        <div>
            ${tmpl_context.widget(value=value_list, action=mount_point+'.json')|n}
        </div>

        ${admin_helpers.link_button(u'/admin', u"Page d'accueil de l'admin", u"Retour à la page d'accueil")}
    </div>
</div>