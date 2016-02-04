## -*- coding: utf-8 -*-
<%inherit file="local:templates.master"/>

<%def name="title()">
    PyJobs: Sources
</%def>

<section id="sources">

    <h1>Liste des sources aggrégées par pyjobs</h1>
    
    <div>
        pyjobs agrège les données à partir de différents jobboard — ce qu'on appelle « sources ».
        <br>Si une source manque, vous pouvez l'ajouter.
        <a href="https://github.com/pyjobs/crawlers#ajouter-une-source-dannonces">C'est facile et tout est expliqué sur le dépôt github </a>.
        <br>Alors n'hésitez pas à contribuer !
        <hr>
    </div>

    % for source_id in sources:
        <% source = sources[source_id] %>
        <% fields_not_collected = False %>

        <article class="source ${source_id}">

            <h2>
                <a href="${source.url}" target="_blank" title="Se rendre sur le site de ${source.label}">
                    ${source.label}
                </a>

                <img style="max-height: 32px;" src="${source.logo_url}" alt="${source.label}" class="logo"/>

                % if sources_last_crawl[source_id]:
                    <% last_crawl_date = sources_last_crawl[source_id] %>
                    <span class="last-crawl">
                        - Dernière récupération le
                        ${h.french_day(last_crawl_date.weekday()).lower()}
                        ${last_crawl_date.strftime('%d')}
                        ${h.french_month(int(last_crawl_date.strftime('%m'))).lower()}
                        ${last_crawl_date.strftime('%Y')}
                        à
                        ${last_crawl_date.strftime('%Hh%m')}
                    </span>
                % endif

            </h2>

            <p>État des éléments récupérable sur cette source:</p>

            <ul class="fields">
                % for existing_field in existing_fields:
                    % if source.spider_class.has_parameter_for_field(existing_field):
                        <% field_class = 'collected'%>
                        <% field_title = u'Cet élément est collecté'%>
                    % else:
                        <% field_class = 'not-collected'%>
                        <% field_title = u'Cet élément n\'est pas encore collecté'%>
                        <% fields_not_collected = True %>
                    % endif
                    <li class="btn label field ${field_class}" title="${field_title}">
                        ${existing_field}
                    </li>
                % endfor
            </ul>

            % if fields_not_collected:
                <a href="https://github.com/pyjobs/crawlers"
                   target="_blank"
                   class="btn btn-success improve">
                    Améliorer ${source.label} sur PyJobs
                </a>
            % endif

        </article>

    % endfor

</section>