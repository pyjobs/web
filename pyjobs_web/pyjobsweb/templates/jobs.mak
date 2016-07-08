<%inherit file="local:templates.master"/>
<%!
    import urllib

    def encode_object(value):
        if type(value) in (str, unicode):
            return value.encode('utf-8')

%>

<%def name="job_pagination()">\
    <div class="row">
        <div class="col-sm-12">
            <ul class="pagination">
                    ${tmpl_context.paginators.jobs.pager(format='$link_first $link_previous <li><span>Page $page / $page_count</span></li> $link_next $link_last', page_link_template='<li><a %s>%s</a></li>', page_plain_template='<li><span%s>%s</span></li>', symbol_first=u'<< début', symbol_last=u'fin >>', symbol_previous=u'< précédente', symbol_next=u'suivante >', show_if_single_page=True)}
            </ul>
        </div>
    </div>
</%def>

<%def name="title()">
    pyjobs — le job qu'il vous faut en python
</%def>

<div class="row">
    <div class="col-md-12">
        <div class="page-header">
            <h1>
                Le job qu'il vous faut &mdash; en python
                <span class="btn-group pull-right" role="group">
##                     <button type="button" class="btn btn-default">
##                         <i class="fa fa-3x fa-twitter" style="color: #55ACEE;"></i>
##                     </button>
                    <a href="/rss?limit=50" title="Flux RSS des annonces de jobs python" class="btn btn-warning">
                        <i class="fa fa-3x fa-rss"></i>
                    </a>

                    <a href="https://github.com/pyjobs/annonces" title="Annonces sur GitHub" class="btn btn-default">
                        <i class="fa fa-3x fa-github"></i>
                    </a>
                </span>

            </h1>
##             <h2>
##                 <div class="row">
##                     <div class="col-md-6">
##                         <div class="input-group">
##                             <input type="text" class="form-control" placeholder="Search for a job...">
##                             <span class="input-group-btn">
##                                 <button class="btn btn-default" type="button">Go!</button>
##                             </span>
##                         </div>
##                     </div>
##                     <div class="col-md-6">
##                         <div class="btn-group" role="group" aria-label="...">
##                             <button type="button" class="btn btn-small btn-default">Ma boîte recrute</button>
##                             <button type="button" class="btn btn-small btn-default">Publier une annonce</button>
##                         </div>
##                     </div>
##                 </div>
##             </h2>
        </div>
    </div>
</div>

<div id="research_form" class="row">
    ${job_offer_search_form.display()|n}
</div>

${job_pagination()}

% if not jobs:
    <h3>Désolé, aucune offre d'emploi n'a  pu être trouvée.</h3>
% else:
    <div class = "row">
        % for job in jobs:
            <div class="col-md-12">
                <div id="job-post-${job.id}" class="job-item ${loop.cycle('row-even', 'row-odd')}" style="padding: 1em 1em 3em 1em;">
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
                                    <img style="max-height: 32px;" src="${sources[job.source].logo_url}" alt="${sources[job.source].label}"/>
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
            </div>
            <div class="col-md-3">
            </div>
        % endfor
    </div>
% endif

${job_pagination()}


