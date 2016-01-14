<%inherit file="local:templates.master"/>

<h1>
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

<p>
    ${job.description|n}
</p>
