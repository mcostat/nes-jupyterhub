# Configuration file for jupyterhub.

import os

c = get_config()  # noqa

c.JupyterHub.authenticator_class = "generic-oauth"

c.GenericOAuthenticator.client_id = os.getenv(
    "CLIENT_ID", "tIaWTGDij1MnwZFivsqklGgBfqk8fr7saty5Zvid"
)
c.GenericOAuthenticator.client_secret = os.getenv(
    "CLIENT_SECRET",
    "D5zJd1oy90wRLxfvMnDu80GbV7E6KIHynn5r9TsMT3XNhEAgIokZvZFoXEQoYUSDeDoupQZxEeXRfuPuyc4yDJ4XDvxuQVreMFlGkv2I3AWw6y1rNXAq1CZvEaKPdMkp",
)
c.GenericOAuthenticator.login_service = "NES"

c.OAuthenticator.oauth_callback_url = os.getenv(
    "CALLBACK_URL", "http://localhost:8000/hub/oauth_callback"
)
c.GenericOAuthenticator.authorize_url = os.getenv(
    "AUTHORIZE_URL", "http://localhost/o/authorize/"
)
c.GenericOAuthenticator.token_url = os.getenv("TOKEN_URL", "http://nes/o/token/")
c.GenericOAuthenticator.userdata_url = os.getenv(
    "USERDATA_URL", "http://nes/o/userinfo/"
)

c.OAuthenticator.allow_all = True
c.OAuthenticator.allow_existing_users = True
c.OAuthenticator.admin_users = {"nes_admin"}

c.OAuthenticator.basic_auth = True

c.JupyterHub.hub_connect_ip = "jupyterhub"


c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8081


c.JupyterHub.internal_ssl = True

c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

c.DockerSpawner.remove = True
c.DockerSpawner.network_name = os.environ.get("DOCKER_NETWORK_NAME", "nes-network")
c.DockerSpawner.use_internal_ip = True

notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# c.DockerSpawner.image = 'jupyter/base-notebook'


## Path to SSL certificate file for the public facing interface of the proxy
#
#          When setting this, you should also set ssl_key
#  Default: ''
# c.JupyterHub.ssl_cert = ''

## Path to SSL key file for the public facing interface of the proxy
#
#          When setting this, you should also set ssl_cert
#  Default: ''
# c.JupyterHub.ssl_key = ''

from subprocess import check_call


def my_hook(spawner):
    username = spawner.user.name
    spawner.volumes.update(
        {os.getenv("NES_MEDIA_PATH", "nes_media"): "/home/jovyan/work/data"}
    )

    # os.system("ls -s /nes/media /home/jovyan/work/data")


c.Spawner.pre_spawn_hook = my_hook
