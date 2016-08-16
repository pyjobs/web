<%inherit file="local:templates.master"/>

<%def name="title()">
    pyjobs — ${company.name}
</%def>

<%def name="page_header()">
    <header class="page-header">
        % if request.params.get('previous'):
            <a href="${request.params.get('previous')}"
               title="Retour à la liste des entreprises"
               class="btn btn-default btn-xs" style="margin-bottom: 20px;">
                retour
            </a>
        % endif

        <h1 class="company">
            ${company.name}
        </h1>

        <h4>
            % for technology in company.technologies.split(','):
                <span class="label label-default">${technology}</span>
            % endfor
        </h4>
    </header>
</%def>

<h3>
    Description de l'entreprise:
</h3>

<div class="company-description">
    <br/>
    ${company.description|n}
</div>


<a title="Site web de l'entreprise"
   class="btn btn-primary btn-lg centered-block company-source-link"
   href="${company.url}"
   target="_blank">
    Voir le site web de l'entreprise
</a>
