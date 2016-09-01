<%inherit file="local:templates.master"/>
<%!
    import urllib

    def encode_object(value):
        if type(value) in (str, unicode):
            return value.encode('utf-8')

%>

<%def name="company_pagination()">
    <ul class="pagination">
        ${tmpl_context.paginators.companies.pager(format='$link_first $link_previous <li><span>Page $page / $page_count</span></li> $link_next $link_last', page_link_template='<li><a %s>%s</a></li>', page_plain_template='<li><span%s>%s</span></li>', symbol_first=u'<< début', symbol_last=u'fin >>', symbol_previous=u'< précédente', symbol_next=u'suivante >', show_if_single_page=True)}
    </ul>
</%def>

<%def name="title()">
    pyjobs — le job qu'il vous faut en python
</%def>

<%def name="page_header()">
    <header class="page-header">
        <h1>
            Les entreprises qui recrutent !
            <span class="btn-group pull-right" role="group">
                <a href="/societes-qui-recrutent/new" title="Ajouter une entreprise" class="btn btn-success">
                    <i class="fa fa-3x fa-plus"></i>
                </a>
            </span>
        </h1>
    </header>
</%def>

<div id="company_search_form">
    <h2>Rechercher une entreprise</h2>
     ${company_search_form.display(action='/societes-qui-recrutent/search', method='POST')}
</div>

${company_pagination()}

% if not companies:
    <div class="no-company-found">
        <h3>Désolé, aucune entreprise n'a pu être trouvée.</h3>
    </div>
% else:
    % for company in companies:
        <div id="company-${company.id}" class="company-item ${loop.cycle('row-even', 'row-odd')}"
             style="padding: 1em 1em 3em 1em;">
            <div class="row" id="company-post-head-${company.id}">
                <div class="col-md-9">
                    <h3 style="margin-top: 0; padding-top: 0;">
                        <a style="color: #555; font-weight: bold;"
                           href="${h.get_company_url(company.id, previous=request.url)}">
                            <i style="color: #555;" class="fa fa-fw fa-building-o"></i>
                            ${company.name}
                        </a>
                        <br/>
                        <a href="mailto:${company.url}" style="color: #999;">
                            <i class="fa fa-fw fa-envelope-o"></i>
                            <span style="font-size: 0.9em;">
                                ${company.email}
                            </span>
                        </a>
                        <br/>
                        <span style="color: #999;">
                            <i class="fa fa-fw fa-phone"></i>
                            <span style="font-size: 0.9em;">
                                ${company.phone}
                            </span>
                        </span>
                        <br/>
                        <a href="http://nominatim.openstreetmap.org/search.php?q=${company.address}">
                            <i class="fa fa-fw fa-map-marker"></i>
                            <span style="font-size: 0.9em;">
                                ${company.address}
                            </span>
                        </a>
                    </h3>
                </div>

                <div class="col-md-3">
                    <div class="text-right">
                        <h4>
                            <a href="${company.url}" style="color: #555;">
                                <i class="fa fa-fw fa-external-link"></i>
                                Site de l'entreprise
                            </a>
                            <br/>
                            <a href="${company.url}" style="color: #AAA; font-weight: bold;">
                                <img style="max-height: 32px;" src="${company.logo_url}" alt="${company.name}"/>
                            </a>
                        </h4>
                    </div>
                </div>

                <div class="col-md-12">
                    % for technology in company.technologies.split(', '):
                        <span class="label label-default label-pyjob company-technology">${technology}</span>
                    % endfor
                </div>

                <div class="col-md-12">
                    <h4 style="color: #555;">
                        Présentation de l'entreprise:
                    </h4>
                    <div class="col-md-1"></div>
                    <div class="col-md-10">
                        <h4 style="color: #555; font-size: 1.1em;">
                            ${company.description[0:139].rstrip()}
                            % if len(company.description) > 140:
                                ...
                                <a href="${h.get_company_url(company.id, previous=request.url)}">
                                    (cliquez ici pour lire la suite)
                                </a>
                            % endif
                        </h4>
                    </div>
                </div>
            </div>
        </div>
    % endfor
% endif

${company_pagination()}
