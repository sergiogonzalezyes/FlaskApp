from flask import Blueprint, session, abort, redirect, request
from .auth import Flow, GOOGLE_CLIENT_ID
import requests
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow



main = Blueprint('main', __name__)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@main.route("/Oauth-login")
def login():
    authorization_url, state = Flow.authorization_url()
    session["state"] = state
    print('session ST8', session["state"])

    return redirect(authorization_url)


@main.route("/callback")
def callback():
    Flow.fetch_token(authorization_response=request.url)
    print('request url', request.url)
    print('request args', request.args['state'])
    print('callback state', session["state"])

    session_state = session.get("state")
    if session_state is None or session_state != request.args["state"]:
        abort(500)  # State does not match!

    credentials = Flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    print(session["name"])
    print(session["google_id"])

    return redirect("/protected_area")


@main.route("/protected_area")
@login_is_required
def protected_area():
    return redirect("https://chat4pp.vercel.app/")

