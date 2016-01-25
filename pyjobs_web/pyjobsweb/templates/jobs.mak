<%inherit file="local:templates.master"/>
<%!
    import urllib

    def encode_object(value):
        if type(value) in (str, unicode):
            return value.encode('utf-8')

%>

<%def name="job_pagination()">\
    <div class="row">
        <div class="col-md-12">
            <ul class="pagination">
                ${tmpl_context.paginators.jobs.pager(format='$link_first $link_previous <li><span>Page $page / $page_count</span></li> $link_next $link_last', page_link_template='<li><a %s>%s</a></li>', page_plain_template='<li><span%s>%s</span></li>', symbol_first=u'<< début', symbol_last=u'fin >>', symbol_previous=u'< précédente', symbol_next=u'suivante >', show_if_single_page=True)}
            </ul>
        </div>
    </div>
</%def>

<%def name="title()">
    PyJobs: Le job qu'il vous faut en python
</%def>

    <div class="row">
        <div class="col-md-12">
            <div class="page-header">
                <h1>
                    Le job qu'il vous faut &mdash; en python
                    <div class="btn-group pull-right" role="group">
                        <button type="button" class="btn btn-default"><i class="fa fa-3x fa-twitter" style="color: #55ACEE;"></i></button>
                        <button type="button" class="btn btn-warning"><i class="fa fa-3x fa-rss"></i></button>
                    </div>

                </h1>
##                 <h2>
##                     <div class="row">
##                         <div class="col-md-6">
##                             <div class="input-group">
##                                 <input type="text" class="form-control" placeholder="Search for a job...">
##                                 <span class="input-group-btn">
##                                     <button class="btn btn-default" type="button">Go!</button>
##                                 </span>
##                             </div>
##                         </div>
##                         <div class="col-md-6">
##                             <div class="btn-group" role="group" aria-label="...">
##                                 <button type="button" class="btn btn-small btn-default">Ma boîte recrute</button>
##                                 <button type="button" class="btn btn-small btn-default">Publier une annonce</button>
##                             </div>
##                         </div>
##                     </div>
##                 </h2>
            </div>
        </div>
    </div>

${job_pagination()}

    % for job in jobs:

        <!-- Modal -->
        <div class="modal" id="modal-job-${job.id}" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
          <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title" id="myModalLabel">${job.title}</h4>
              </div>
              <div class="modal-body">
                  <ul>
                      <li>${job.company}</li>
                      <li>${job.address}</li>
                  </ul>
                  <hr/>
                  ${job.description|n}
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary">Save changes</button>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
            <div class="col-md-12">
                <div id="job-post-${job.id}" class="job-item ${loop.cycle('row-even', 'row-odd')}" style="border-top: 1px dotted #DDD; padding: 1em 1em 3em 1em;">
                    <div class="row" id="job-post-head-${job.id}">
                        <div class="col-md-9">
                            <h2 style="margin-top: 0; padding-top: 0; font-size: 1.7em;">
                                <a style="color: #555; font-weight: bold;" data-toggle="modal" data-target="#modal-job-${job.id}" >${job.title}</a>

                                <!-- TODO: TurboGears "url" helper ? -->
                                <a href="/job/${job.id}/${h.slugify(job.title)}">
                                    JOB PAGE
                                </a>

                                % for tag in job.condition_tags:
                                    <span class="label label-default ${tag.css}">${tag.tag}</span>
                                % endfor

                                <br/>
                                <div style="color: #999;">${job.company}</div>
                            </h2>
                        </div>

                        <div class="col-md-3">
                            <div class="text-right">
                                <span style="font-size: 1.5em; font-weight: bold; color: #777;">${job.published}</span><br/>
                                <a href="${sources[job.source].url}" style="color: #AAA; font-weight: bold;">
                                    ${sources[job.source].label}<br/>
                                    <img style="max-height: 32px;" src="${sources[job.source].logo_url}" alt="${sources[job.source].label}"/>
                                </a>

                            </div>
                        </div>
                    </div>
                    <div class="row" id="job-post-detail-${job.id}-detail">
##                            <a href="https://www.google.fr/maps/search/${urllib.quote_plus(encode_object(job.address))}">${job.address}</a>
##                            <p class="label label-warning" style="font-weight: bold; font-size: 1.2em;">${job.address}</p>
##                            <p class="label label-success" style="font-weight: bold; font-size: 1.2em;">${job.company}</p>
                        <div class="col-md-12">
                            % for tag in job.alltags:
                                <span class="label label-default label-pyjob">${tag.tag}</span>
                            % endfor
                        </div>
            ##             <td>
            ##                 <div class="btn-group" role="group" aria-label="...">
            ##                   <button type="button" class="btn btn-small btn-default"><i style="color: #F00;" class="fa fa-fw fa-2x fa-heart"></i></button><button type="button" class="btn btn-small btn-default"><i style="color: #888;" class="fa fa-fw fa-2x fa-trash"></i></button>
            ##                 </div>
            ##             </td>
                    </div>
        ##             <div class="row">
        ##                 ${job.description|n}
        ##             </div>
                </div>
            </div>
            <div class="col-md-3">
            </div>
        </div>
    % endfor

${job_pagination()}


