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
            ${company.name} -

            <a class="inside-link" href="${company.url}" style="color: #555;"
               target="_blank">
                ${company.url.replace('http://', '')}
            </a>
        </h1>
    </header>
</%def>

<div id="company-details-body" class="row">
    <div id="company-address" class="col-sm-8 col-xs-12">
        <h3>Adresse</h3>
        <h4>
            <a class="inside-link"
               href="http://nominatim.openstreetmap.org/search.php?q=${company.address}"
               target="_blank">
                <i class="fa fa-fw fa-map-marker"></i>
                <span style="font-size: 0.9em;">
                    ${company.address}  <!-- Company name !!! -->
                </span>
            </a>

            <!-- TODO
                <span>
                    <br/>
                    <i class="fa fa-fw fa-map-street"></i>
                    Company street
                    <br/>
                    <i class="fa fa-fw fa-map-town"></i>
                    Company CP + Company Town
                    <br/>
                    <i class="fa fa-fw fa-map-country"></i>
                    Company Country
                </span>
            -->
        </h4>
    </div>

    <div id="company-contact" class="col-sm-4 col-xs-12">
        <h3>Informations de contact</h3>
        <h4>
            <a href="mailto:${company.url}" class="inside-link"
               style="color: #999;">
                <i class="fa fa-fw fa-envelope-o"></i>
                <span style="font-size: 0.9em;">
                    ${company.email}
                </span>
            </a>
            <br/>
            <span style="color: #999;">
                <i class="fa fa-fw fa-phone"></i>
                <span style="font-size: 0.9em;">
                    ${company.phone}
                </span>
            </span>
        </h4>
    </div>

    <div id="company-technologies" class="col-xs-12 hidden-sm hidden-md hidden-lg">
        % if company.technologies.split(','):
            <h3>Technologies</h3>
        % endif
        % for i, technology in enumerate(company.technologies.split(',')):
            <span class="label label-info">${technology}</span>
            %if i != 0:
                <br/>
            %endif
        % endfor
    </div>

    <div id="company-description" class="col-sm-8 col-xs-12">
        <h3>
            Description
        </h3>
        <div style="white-space: pre;">${company.description|n}</div>
        <br/>
    </div>

    <div id="company-technologies" class="col-sm-4 hidden-xs">
        % if company.technologies.split(','):
            <h3>Technologies</h3>
        % endif
        % for technology in company.technologies.split(','):
            <h4>
                <span class="label label-info">
                    ${technology}
                </span>
            </h4>
        % endfor
        <br/>
    </div>

    <div id="address_button" class="col-sm-12 hidden-xs">
        <a title="Site web de l'entreprise"
           class="btn btn-primary hidden-xs centered-block company-source-link"
           href="${company.url}"
           target="_blank">
            Visiter le site web de l'entreprise
        </a>
    </div>

    <div id="address_button" class="col-xs-12 hidden-lg">
        <a title="Site web de l'entreprise"
           class="btn btn-primary btn-sm hidden-sm hidden-md hidden-lg centered-block company-source-link"
           href="${company.url}"
           target="_blank">
            Site de l'entreprise
        </a>
    </div>
</div>
