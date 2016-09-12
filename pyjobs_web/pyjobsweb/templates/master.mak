<!DOCTYPE html>
<html class="${self.html_class()}">
    <head>
        ${self.meta()}
        <title>${self.title()}</title>
        <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/bootstrap.min.css')}"/>
        <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/select2.css')}"/>
        <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/select2.bootstrap.css')}"/>
        <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}"/>
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
        <link rel="alternate" type="application/rss+xml" title="RSS" href="/rss?limit=50"/>
        ${self.head_content()}
        ${h.head_js() | n}
    </head>

    <body class="${self.body_class()}">
        ${self.main_menu()}
        <div class="container full-height">
            ${self.content_wrapper()}
            ${self.footer()}
        </div>
        ${self.end_body_scripts()}
    </body>

    <%def name="content_wrapper()">
        <%
            flash=tg.flash_obj.render('flash', use_js=False)
        %>
        % if flash:
            ${flash | n}
        % endif
        ${self.page_header()}
        ${self.body()}
    </%def>

    <%def name="page_header()"></%def>
    <%def name="html_class()"></%def>
    <%def name="body_class()"></%def>
    <%def name="container_class()"></%def>
    <%def name="meta()">
        <meta charset="${response.charset}"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </%def>
    <%def name="head_content()"></%def>

    <%def name="title()">  </%def>

    <%def name="end_body_scripts()">
        <script src="http://code.jquery.com/jquery.js"></script>
        <script src="${tg.url('/javascript/select2.min.js')}"></script>
        <script src="${tg.url('/javascript/select2_locale_fr.js')}"></script>
        <script src="${tg.url('/javascript/bootstrap.min.js')}"></script>
        <script src="${tg.url('/javascript/clickable_divs.js')}"></script>
        <script src="${tg.url('/javascript/helpers.js')}"></script>
    </%def>

    <%def name="footer()">
        <footer class="row footer hidden-xs hidden-sm">
            <p>Copyright &copy; ${getattr(tmpl_context, 'project_name', 'Algoo')} ${h.current_year()}</p>
        </footer>
    </%def>

    <%def name="main_menu()">
        <!-- Navbar -->
        <nav class="navbar navbar-default navbar-static-top" role="navigation">
            <div class="container">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar-content">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand" href="${tg.url('/')}">
                        <div style="display: inline-block">
                            <img src="${tg.url('/img/pyjobs_logo_square.png')}" style="height: 32px;" alt="pyjobs"/>
                            pyjobs
                        </div>
                        <div class="hidden-xs hidden-sm hidden-md" style="display: inline-block">
                            &mdash;<small>opportunités professionnelles python</small>
                        </div>
                    </a>
                </div>

                <div class="collapse navbar-collapse" id="navbar-content">
                    <ul class="nav navbar-nav navbar-right">
                        <!--
                            <li class="${('', 'active')[page=='index']}"><a href="${tg.url('/recruteurs')}">Recruteurs</a></li>
                            <li class="${('', 'active')[page=='about']}"><a href="${tg.url('/candidats')}">Candidats</a></li>
                            <li class="${('', 'active')[page=='data']}"><a href="${tg.url('/about')}">A propos</a></li>
                        -->
                    </ul>

                    % if tg.auth_stack_enabled:
                        <ul class="nav navbar-nav navbar-right">
                            ##         <li class="${('', 'active')[page=='index']}"><a href="${tg.url('/recruteurs')}">Recruteurs</a></li>
                            ##         <li class="${('', 'active')[page=='about']}"><a href="${tg.url('/candidats')}">Candidats</a></li>
                            <li class="${('', 'active')[page=='index']}">
                                <a href="${tg.url('/societes-qui-recrutent')}">
                                    Les entreprises qui recrutent
                                </a>
                            </li>
                            <li class="${('', 'active')[page=='index']}">
                                <a href="${tg.url('/origine-des-annonces-diffusees')}">
                                    Origine des annonces
                                </a>
                            </li>
                            <li class="${('', 'active')[page=='stats']}">
                                <a href="${tg.url('/stats')}">
                                    Statistiques
                                </a>
                            </li>
                            <li class="${('', 'active')[page=='about']}">
                                <a href="${tg.url('/about')}">
                                    À propos
                                </a>
                            </li>
                            ##       <li class="${('', 'active')[page=='data']}"><a href="${tg.url('/about')}">A propos</a></li>
                            ##       % if not request.identity:
                            ##         <li><a href="${tg.url('/login')}">Login</a></li>
                            ##       % else:
                            ##         <li><a href="${tg.url('/logout_handler')}">Logout</a></li>
                            ##         <li><a href="${tg.url('/admin')}">Admin</a></li>
                            ##       % endif
                        </ul>
                    % endif
                </div>
            </div>
        </nav>
    </%def>

</html>
