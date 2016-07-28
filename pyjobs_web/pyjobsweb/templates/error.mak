<%inherit file="local:templates.master"/>

<%def name="title()">
    pyjobs — erreur
</%def>

<%def name="page_header()">
    <header class="page-header">
        <h1>Error ${code}</h1>
    </header>
</%def>

<%
    import re
    mf = re.compile(r'(</?)script', re.IGNORECASE)
    def fixmessage(message):
        return mf.sub(r'\1noscript', message)
%>

<div>${fixmessage(message) | n}</div>

