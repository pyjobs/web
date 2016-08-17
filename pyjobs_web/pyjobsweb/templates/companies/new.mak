<%inherit file="local:templates.master"/>
<%!
    import urllib

    def encode_object(value):
        if type(value) in (str, unicode):
            return value.encode('utf-8')

%>

<%def name="title()">
    pyjobs — le job qu'il vous faut en python
</%def>

<%def name="page_header()">
    <header class="page-header">
        <h1>
            Formulaire de création d'entreprise
        </h1>
    </header>
</%def>

<div id="new_company_form" class="row">
    ${new_company_form.display()|n}
</div>
