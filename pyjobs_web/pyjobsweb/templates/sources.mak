## -*- coding: utf-8 -*-
<%inherit file="local:templates.master"/>

<section id="sources">

    <h1>PyJobs sources</h1>

    % for source_id in sources:
        <% source = sources[source_id] %>
        <% fields_not_collected = False %>

        <article class="source">

            <h2>
                <a href="${source.url}" target="_blank" title="Se rendre sur le site de ${source.label}">
                    ${source.label}
                </a>
                <img style="max-height: 32px;" src="${source.logo_url}" alt="${source.label}"/>
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