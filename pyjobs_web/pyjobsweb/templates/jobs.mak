<%inherit file="local:templates.master"/>
<%!
    import urllib

    def encode_object(value):
        if type(value) in (str, unicode):
            return value.encode('utf-8')

%>

<%def name="job_pagination()">
    <ul class="pagination">
        ${tmpl_context.paginators.jobs.pager(format='$link_first $link_previous <li><span>Page $page / $page_count</span></li> $link_next $link_last', page_link_template='<li><a %s>%s</a></li>', page_plain_template='<li><span%s>%s</span></li>', symbol_first=u'<< début', symbol_last=u'fin >>', symbol_previous=u'< précédente', symbol_next=u'suivante >', show_if_single_page=True)}
    </ul>
</%def>

<%def name="title()">
    pyjobs — le job qu'il vous faut en python
</%def>

<%def name="page_header()">
    <header class="page-header">
        <h1>
            Le job qu'il vous faut &mdash; en python
            <span class="btn-group pull-right" role="group">
                <a href="https://twitter.com/pyjobsfr" title="Annonces sur Twitter" target="_blank" class="btn btn-default">
                    <i class="fa fa-3x fa-twitter" style="color: #55ACEE;"></i>
                </a>

                <a href="/rss?limit=50" title="Flux RSS des annonces de jobs python" target="_blank" class="btn btn-warning">
                    <i class="fa fa-3x fa-rss"></i>
                </a>

                <a href="https://github.com/pyjobs/annonces" title="Annonces sur GitHub" target="_blank" class="btn btn-default">
                    <i class="fa fa-3x fa-github"></i>
                </a>

                <a href="/company/new" title="Ajouter une entreprise" class="btn btn-default">
                    <i class="fa fa-3x fa-plus"></i>
                </a>
            </span>
        </h1>
    ##    <h2>
    ##            <div class="col-md-6">
    ##                <div class="btn-group" role="group" aria-label="...">
    ##                    <button type="button" class="btn btn-small btn-default">Ma boîte recrute</button>
    ##                    <button type="button" class="btn btn-small btn-default">Publier une annonce</button>
    ##                </div>
    ##            </div>
    ##        </div>
    ##    </h2>
    </header>
</%def>

<div id="research_form">
    ${job_offer_search_form.display()|n}
</div>

${job_pagination()}

% if not jobs:
    <div class="no-job-found">
        <h3>Désolé, aucune offre d'emploi n'a pu être trouvée.</h3>
    </div>
% else:
    % for job in jobs:
        <div id="job-post-${job.id}" class="job-item ${loop.cycle('row-even', 'row-odd')}"
             style="padding: 1em 1em 3em 1em;">
            <div class="row" id="job-post-head-${job.id}">
                <div class="col-md-9">
                    <h2 style="margin-top: 0; padding-top: 0; font-size: 1.7em;">
                        <a style="color: #555; font-weight: bold;"
                           href="${h.get_job_url(job.id, job.title, previous=request.url)}">
                            ${job.title}
                        </a>

                        % for tag in job.condition_tags:
                            <span class="label label-default job-tag ${tag.css}">${tag.tag}</span>
                        % endfor

                        <br/>
                            <span style="color: #999;">
                                <i class="fa fa-fw fa-building-o"></i> ${job.company}
                                <br/>
                                <a href="http://nominatim.openstreetmap.org/search.php?q=${job.address | u}">
                                    <i class="fa fa-fw fa-map-marker"></i>
                                    ${job.address}
                                </a>
                            </span>
                    </h2>
                </div>

                <div class="col-md-3">
                    <div class="text-right">
                            <span style="font-size: 1.5em; font-weight: bold; color: #777;">
                                ${job.published}
                                % if job.publication_datetime_is_fake:
                                    <span class="warning" title="Cette date n'est peut-être pas fiable">
                                        &#9888;
                                    </span>
                                % endif
                            </span>
                        <br/>
                        <a href="${sources[job.source].url}" style="color: #AAA; font-weight: bold;">
                            ${sources[job.source].label}<br/>
                            <img style="max-height: 32px;" src="${sources[job.source].logo_url}"
                                 alt="${sources[job.source].label}"/>
                        </a>
                    </div>
                </div>
            </div>
            <div class="row" id="job-post-detail-${job.id}-detail">
                ##                        <a href="https://www.google.fr/maps/search/${urllib.quote_plus(encode_object(job.address))}">${job.address}</a>
                ##                        <p class="label label-warning" style="font-weight: bold; font-size: 1.2em;">${job.address}</p>
                ##                        <p class="label label-success" style="font-weight: bold; font-size: 1.2em;">${job.company}</p>

                <div class="col-md-12">
                    % for tag in job.alltags:
                        <span class="label label-default label-pyjob job-tag">${tag.tag}</span>
                    % endfor
                </div>
                ##                        <td>
                ##                            <div class="btn-group" role="group" aria-label="...">
                ##                                <button type="button" class="btn btn-small btn-default"><i style="color: #F00;" class="fa fa-fw fa-2x fa-heart"></i></button><button type="button" class="btn btn-small btn-default"><i style="color: #888;" class="fa fa-fw fa-2x fa-trash"></i></button>
                ##                            </div>
                ##                        </td>
                                </div>
            ##                    <div class="row">
            ##                        ${job.description|n}
            ##                    </div>
                        </div>
    % endfor
% endif

${job_pagination()}
