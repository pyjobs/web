<%inherit file="local:templates.master"/>
<%def name="title()">Login Form</%def>

<%def name="page_header()">
    <header class="page-header">
        <h1>Login</h1>
    </header>
</%def>

<form action="${tg.url('/login_handler', params=dict(came_from=came_from, __logins=login_counter))}"
      method="post" accept-charset="UTF-8" class="form-horizontal">
    <div class="form-group">
        <label class="col-sm-2 control-label">Username:</label>
        <div class="col-sm-7">
            <input class="form-control" type="text" name="login" value="${login}"/>
        </div>
    </div>
    <div class="form-group">
        <label class="col-sm-2 control-label">Password:</label>
        <div class="col-sm-7">
            <input class="form-control" type="password" name="password"/>
        </div>
    </div>
    <div class="form-group">
        <div class="col-sm-7 col-sm-offset-2">
            <div class="checkbox">
                <label>
                    <input type="checkbox" name="remember" value="2252000"/> remember me
                </label>
            </div>
        </div>
    </div>
    <div class="form-group">
        <div class="col-sm-7 col-sm-offset-2">
            <button type="submit" class="btn btn-default">Login</button>
        </div>
    </div>
</form>
