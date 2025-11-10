from flask import Flask, Response, url_for, render_template, request, make_response
import json
import socket

from commonlib.initproperties import InitProperties

# Initialize Flask related properties
webapp_properties = InitProperties('Properties.ini').webapp()
app = Flask(__name__)

PLAIN_TEXT_AGENTS = [
    "curl",
    "httpie",
    "lwp-request",
    "wget",
    "python-requests",
    "python-httpx",
    "openbsd ftp",
    "powershell",
    "fetch",
    "aiohttp",
    "http_get",
    "xh",
]


# Used for stubbing
def stub_test():
    return True


# Helper method for site-map
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


# Root, uses render_templete to generate HTML with CSS styling
@app.route('/')
def index():
    return render_template('index.html')


# Sample JSON response
@app.route("/json-response")
def json_response():
    body = {
        'name': 'John Dela Cruz',
        'age': 25
    }
    response_object = Response(
        response=json.dumps(body),
        mimetype='application/json'
    )
    response_object.headers['Trace'] = socket.gethostname()
    return response_object


# Shows the different routes
@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return links


@app.route("/cli")
def cli():

    parsed_query = {
        'user_agent': request.headers.get('User-Agent', '').lower()
    }

    user_agent = parsed_query.get('user_agent', '').lower()
    is_html = not any(agent in user_agent for agent in PLAIN_TEXT_AGENTS)

    if is_html:
        return render_template('index.html')
    else:
        response = make_response(f"From CLI\n", 200)
        response.mimetype = "text/plain"
        return response


if __name__ == '__main__':
    app.run(host=webapp_properties['host'], port=webapp_properties['port'])