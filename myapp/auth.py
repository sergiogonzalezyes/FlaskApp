import os
import pathlib
from google_auth_oauthlib.flow import Flow


secret_key = os.environ.get("SECRET_KEY")
print("secret_key: ", secret_key)

# To allow HTTP traffic for local development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

print("client_secrets_file: ", client_secrets_file)

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://chat4pp.onrender.com/callback"
)