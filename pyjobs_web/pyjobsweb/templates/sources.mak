## -*- coding: utf-8 -*-
<%inherit file="local:templates.master"/>

<%def name="title()">
    pyjobs — sources
</%def>

<%def name="page_header()">
    <header class="page-header">
        <h1>Liste des sources aggrégées par pyjobs</h1>
        <p>pyjobs agrège les annonces concernant la technologie python à partir de différents jobboards. Vous trouverez ci-dessous la liste des différents jobboards pris en charge par pyjobs, ainsi que le niveau de détail des informations prises en charge.</p>
        <p>Un site manque ? Ce n'est pas un problème. pyjobs est un logiciel libre auquel vous êtes invités à

        <a href="https://github.com/pyjobs/crawlers#ajouter-une-source-dannonces">contribuer</a>
        :)
        </p>
    </header>
</%def>

% for source_id in sources:
    <div class="col-sm-12">
        <article class="source ${source_id}">
            <div class="panel panel-default  col-md-7 col-sm-9 col-xs-12">
                <div class="panel-body">
                    <% source = sources[source_id] %>
                    <% fields_not_collected = False %>
                    <h2>
                        <img style="max-height: 32px;"
                             src="${source.logo_url}"
                             alt="${source.label}"
                             class="logo pull-right"
                        />
                        <a href="${source.url}" target="_blank" title="Se rendre sur le site de ${source.label}">
                            ${source.label}
                        </a>
                    </h2>
                    <p>
                        % if sources_last_crawl[source_id]:
                        <% last_crawl_date = sources_last_crawl[source_id] %>
                            <span class="last-crawl-label">dernière mise à jour&nbsp;:</span>
                                <span class="last-crawl pull-right">
                                    ${h.french_day(last_crawl_date.weekday()).lower()}
                                    ${last_crawl_date.strftime('%d')}
                                    ${h.french_month(int(last_crawl_date.strftime('%m'))).lower()}
                                    ${last_crawl_date.strftime('%Y')}
                                    à ${last_crawl_date.strftime('%Hh%m')}</span>
                            </span>
                        % endif
                    </p>
                    <p>
                        % for existing_field in existing_fields:
                        % if source.spider_class.has_parameter_for_field(existing_field):
                            <% field_class = 'label-success'%>
                            <% field_title = u'Cette information est collectée'%>
                            <% icon = u''%>
                        % else:
                            <% field_class = 'label-default'%>
                            <% field_title = u'Cette information n\'est pas encore collectée'%>
                            <% icon = u'  <i class="fa fa-fw fa-warning"></i>'%>
                            <% fields_not_collected = True %>
                        % endif
                            <span class="label ${field_class}" title="${field_title}">${existing_field}${icon|n}</span>
                        % endfor
                    </p>
                    <p class="text-right"><br/>
                        % if fields_not_collected:
                            <a href="https://github.com/pyjobs/crawlers"
                               target="_blank"
                               class="btn btn-primary improve">
                                Améliorer la collecte d'informations depuis
                                    <span class="badge">${source.label}</span>
                            </a>
                        % endif
                    </p>
                </div>
            </div>
        </article>
    </div>
% endfor

<div class="row"></div>
