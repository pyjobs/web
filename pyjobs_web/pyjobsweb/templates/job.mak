<%inherit file="local:templates.master"/>

<%def name="head_content()">
    <link rel="canonical" href="${h.get_job_url(job.id, job.title, absolute=True)}" />
</%def>

<%def name="title()">
    pyjobs — ${job.title}
</%def>

% if request.params.get('previous'):
    <a href="${request.params.get('previous')}"
       title="Retour à la page de listes"
       class="btn btn-default btn-xs">
        retour
    </a>
% endif


<h1 class="job">
    ${job.title}

    % for tag in job.alltags:
        <span class="label label-default ${tag.css}">${tag.tag}</span>
    % endfor

    % for tag in job.condition_tags:
        <span class="label label-default ${tag.css}">${tag.tag}</span>
    % endfor
</h1>

<p class="lead job_content">

    <span class="published">
        ${job.published}
        % if job.publication_datetime_is_fake:
            <span class="warning" title="Cette date n'est peut-être pas fiable">
                 &#9888;
            </span>
        % endif
    </span>

    -

    <span class="company">
        % if job.company_url:
            <a href="${job.company_url}" title="Site internet de ${job.company}">
                ${job.company}
            </a>
        % else:
            ${job.company}
        % endif
    </span>

</p>

<div class="job-description">
    ${job.description|n}
</div>

<a title="Page d'origine de l'annonce"
   class="btn btn-primary btn-lg centered-block job-source-link"
   href="${job.url}"
    target="_blank">
    Voir l'annonce d'origine
</a>
