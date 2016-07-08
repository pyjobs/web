<%inherit file="local:templates.master"/>

<%def name="title()">
    pyjobs — erreur
</%def>

<header class="page-header">
    <div class="container">
        <h1>Error ${code}</h1>
    </div>
</header>

<div class="container">
    <%
    import re
    mf = re.compile(r'(</?)script', re.IGNORECASE)
    def fixmessage(message):
        return mf.sub(r'\1noscript', message)
    %>

    <div>${fixmessage(message) | n}</div>
</div>
