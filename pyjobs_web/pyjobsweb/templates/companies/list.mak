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
    <header class="page-header hidden-xs">
        <h1>
            Les entreprises qui recrutent !
            <span class="btn-group pull-right" role="group">
                <a href="/societes-qui-recrutent/new"
                   title="Ajouter une entreprise" class="btn btn-success">
                    <i class="fa fa-3x fa-plus"></i>
                </a>
            </span>
        </h1>

        <br/>

        <p>Retrouvez ici les entreprises qui recrutent des compétences
            python.</p>
        <p>Si vous êtes vous-même collaborateur d'une entreprise qui recrute ou
            peut-être amenée à recruter des compétences python, n'hésitez pas à
            inscrire votre entreprise !</p>
    </header>

    <header class="page-header hidden-sm hidden-md hidden-lg">
        <h1>
            Les entreprises qui recrutent !
        </h1>
        <span class="btn-group" role="group">
            <a href="/societes-qui-recrutent/new" title="Ajouter une entreprise"
               class="btn btn-success">
                <i class="fa fa-3x fa-plus"></i>
            </a>
        </span>

        <br/>

        <p>Retrouvez ici les entreprises qui recrutent des compétences
            python.</p>
        <p>Si vous êtes vous-même collaborateur d'une entreprise qui recrute ou
            peut-être amenée à recruter des compétences python, n'hésitez pas à
            inscrire votre entreprise !</p>
    </header>
</%def>

<div id="company_search_form">
    <h2>Rechercher une entreprise</h2>
     ${company_search_form.display(action='/societes-qui-recrutent/search', method='POST')}
</div>

${company_pagination()}

<%def name="end_body_scripts()">
    ${parent.end_body_scripts()}

    <script type="text/javascript">
        $(document).ready(function () {
            $(".clickable-div").click(function(e) {
                if (e.ctrlKey) {
                    window.open($(this).find("a:last").attr("href"), "_blank");
                } else {
                    window.location.href = $(this).find("a:last").attr("href");
                    return false;
                }
            });

            $(".clickable-div").hover(function () {
                $(this).attr("title", $(this).find("a:last").attr("href"));
                window.status = $(this).find("a:last").attr("href");
            });

            $(".clickable-div").css("cursor", "pointer");

            $(".inside-link").click(function(event){
                event.stopImmediatePropagation();
            });
        });
    </script>
</%def>

% if not companies:
    <div class="no-company-found">
        <h3>Désolé, aucune entreprise n'a pu être trouvée.</h3>
    </div>
% else:
    % for company in companies:
        <div id="company-${company.id}" class="clickable-div company-item ${loop.cycle('row-even', 'row-odd')}"
             style="padding: 1em 1em 3em 1em;">
            <div class="row" id="company-post-head-${company.id}">
                <div class="col-md-9">
                    <h3 style="margin-top: 0; padding-top: 0;">
                        <a style="color: #555; font-weight: bold;"
                           class="inside-link"
                           href="${h.get_company_url(company.id, previous=request.url)}">
                            <i style="color: #555;" class="fa fa-fw fa-building-o"></i>
                            ${company.name}
                        </a>
                        <br/>
                        <a class="inside-link"
                           href="http://nominatim.openstreetmap.org/search.php?q=${company.address}" target="_blank">
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
                            <a class="inside-link" href="${company.url}" style="color: #AAA; font-weight: bold;" target="_blank">
                                <img style="max-height: 32px;" src="${company.logo_url}" alt="${company.name}"/>
                            </a>
                            <br/>
                            <a class="inside-link" href="${company.url}" style="color: #555;" target="_blank">
                                ${company.url.replace('http://', '')}
                            </a>
                        </h4>
                    </div>
                </div>

                <div class="col-md-12">
                    % for technology in company.technologies.split(', '):
                        <span class="label label-default label-pyjob company-technology">${technology}</span>
                    % endfor
                </div>
            </div>
            <a target="_blank" href="${h.get_company_url(company.id, previous=request.url)}"></a>
        </div>
    % endfor
% endif

${company_pagination()}
