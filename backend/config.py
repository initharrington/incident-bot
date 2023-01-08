import logging
import os

from dotenv import load_dotenv
from typing import List

__version__ = "v0.12.1"

# .env parse
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)
log_level = os.getenv("LOGLEVEL", "INFO").upper()

# Create the logging object
# This is used by submodules as well
logger = logging.getLogger(__name__)


"""
Global Variables
"""
is_test_environment = os.getenv("TEST_ENVIRONMENT", default="false") in (
    "True",
    "true",
    True,
)
templates_directory = os.getenv(
    "TEMPLATES_DIRECTORY", default="templates/slack/"
)

"""
Database Settings
"""
database_host = os.getenv("POSTGRES_HOST")
database_name = os.getenv("POSTGRES_DB")
database_password = os.getenv("POSTGRES_PASSWORD")
database_port = os.getenv("POSTGRES_PORT")
database_user = os.getenv("POSTGRES_USER")
database_url = f"postgresql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"

"""
Incidents Module
"""
incidents_digest_channel = os.getenv("INCIDENTS_DIGEST_CHANNEL")

## Options
incident_auto_create_from_react_enabled = os.getenv(
    "INCIDENT_AUTO_CREATE_FROM_REACT_ENABLED", default="false"
)
incident_auto_create_from_react_emoji_name = os.getenv(
    "INCIDENT_AUTO_CREATE_FROM_REACT_EMOJI_NAME", default=""
)
incident_auto_group_invite_enabled = os.getenv(
    "INCIDENT_AUTO_GROUP_INVITE_ENABLED", default="false"
)
incident_auto_group_invite_group_name = os.getenv(
    "INCIDENT_AUTO_GROUP_INVITE_GROUP_NAME", default=""
)


"""
Slack
"""
slack_app_token = os.getenv("SLACK_APP_TOKEN")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
slack_user_token = os.getenv("SLACK_USER_TOKEN")

"""
Statuspage Module
"""
statuspage_api_key = os.getenv("STATUSPAGE_API_KEY", default="")
statuspage_integration_enabled = os.getenv(
    "STATUSPAGE_INTEGRATION_ENABLED", default="false"
)
statuspage_page_id = os.getenv("STATUSPAGE_PAGE_ID", default="")
statuspage_url = os.getenv("STATUSPAGE_URL", default="")

"""
Confluence
"""
confluence_api_url = os.getenv("CONFLUENCE_API_URL", default="")
confluence_api_username = os.getenv("CONFLUENCE_API_USERNAME", default="")
confluence_api_token = os.getenv("CONFLUENCE_API_TOKEN", default="")
confluence_space = os.getenv("CONFLUENCE_SPACE", default="")
confluence_parent_page = os.getenv("CONFLUENCE_PARENT_PAGE", default="")
auto_create_rca = os.getenv("AUTO_CREATE_RCA", default="false")

"""
PagerDuty
"""
pagerduty_integration_enabled = os.getenv(
    "PAGERDUTY_INTEGRATION_ENABLED", default="false"
)
pagerduty_api_username = os.getenv("PAGERDUTY_API_USERNAME", default="")
pagerduty_api_token = os.getenv("PAGERDUTY_API_TOKEN", default="")

"""
External
"""
auto_create_zoom_meeting = os.getenv("ZOOM_AUTO_CREATE", default="false")
zoom_account_id = os.getenv("ZOOM_ACCOUNT_ID", default="")
zoom_client_id = os.getenv("ZOOM_CLIENT_ID", default="")
zoom_client_secret = os.getenv("ZOOM_CLIENT_SECRET", default="")

"""
Web Application
"""
jwt_secret_key = os.getenv("JWT_SECRET_KEY")
default_admin_password = os.getenv("DEFAULT_WEB_ADMIN_PASSWORD")
flask_debug_mode = os.getenv("FLASK_DEBUG_MODE_ENABLED", default="false") in (
    "True",
    "true",
    True,
)

"""
Helper Methods
"""


def env_check(required_envs: List[str]):
    """Check for the existence of required env vars

    Keyword arguments:
    required_envs -- List[str] containing vars to check
    """
    logger.info("Running env check...")
    for e in required_envs:
        if os.getenv(e) == "":
            logger.fatal(f"The environment variable {e} cannot be empty.")
            exit(1)
        else:
            pass
    if auto_create_zoom_meeting in ("True", "true", True):
        for var in [
            "ZOOM_ACCOUNT_ID",
            "ZOOM_CLIENT_ID",
            "ZOOM_CLIENT_SECRET",
        ]:
            if os.getenv(var) == "":
                logger.fatal(
                    f"If enabling Zoom meeting auto-create, the {var} variable must be set."
                )
                exit(1)
    if auto_create_rca in ("True", "true", True):
        for var in [
            "CONFLUENCE_API_URL",
            "CONFLUENCE_API_USERNAME",
            "CONFLUENCE_API_TOKEN",
            "CONFLUENCE_SPACE",
            "CONFLUENCE_PARENT_PAGE",
        ]:
            if os.getenv(var) == "":
                logger.fatal(
                    f"If enabling the Confluence integration to auto create an RCA, the {var} variable must be set."
                )
                exit(1)
    if incident_auto_create_from_react_enabled in ("True", "true", True):
        if incident_auto_create_from_react_emoji_name == "":
            logger.fatal(
                f"If enabling auto create via react, the INCIDENT_AUTO_CREATE_FROM_REACT_EMOJI_NAME variable must be set."
            )
            exit(1)
    if incident_auto_group_invite_enabled in ("True", "true", True):
        if incident_auto_group_invite_group_name == "":
            logger.fatal(
                f"If enabling auto group invite, the INCIDENT_AUTO_GROUP_INVITE_GROUP_NAME variable must be set."
            )
            exit(1)
    if pagerduty_integration_enabled in ("True", "true", True):
        for var in [
            "PAGERDUTY_API_USERNAME",
            "PAGERDUTY_API_TOKEN",
        ]:
            if os.getenv(var) == "":
                logger.fatal(
                    f"If enabling the PagerDuty integration, the {var} variable must be set."
                )
                exit(1)
    if statuspage_integration_enabled in ("True", "true", True):
        for var in [
            "STATUSPAGE_API_KEY",
            "STATUSPAGE_PAGE_ID",
            "STATUSPAGE_URL",
        ]:
            if os.getenv(var) == "":
                logger.fatal(
                    f"If enabling the Statuspage integration, the {var} variable must be set."
                )
                exit(1)


def slack_template_check(required_templates: List[str]):
    """Check for the existence of the required Slack message
    directory and json templates

    Keyword arguments:
    required_templates -- List[str] containing the names of required
    json files in the templates_directory
    """
    logger.info("Running Slack template check...")
    if os.path.isdir(templates_directory):
        logger.info(f"Templates directory found: {templates_directory}")
    else:
        logger.fatal(
            f"Templates directory not found - {templates_directory} was specified as the location."
        )
        exit(1)
    for rt in required_templates:
        if os.path.isfile(f"{templates_directory}/{rt}"):
            logger.debug(f"Found {rt}")
        else:
            logger.fatal(
                f"{rt} is a required template and is missing from the templates directory: {templates_directory}"
            )
            exit(1)
    logger.info("All templates found successfully.")


def startup_message(workspace: str, wrap: bool = False) -> str:
    """
    Returns diagnostic info for startup or troubleshooting
    """
    msg = f"""
--------------------------------------------------------------------------------
                            incident bot {__version__}
--------------------------------------------------------------------------------
Core functionality:
    Database host:                      {database_host}
    Incidents digest channel:           {incidents_digest_channel}
    Slack workspace:                    {workspace}
    Logging level:                      {log_level}

Options:
    Auto create RCA doc:                {auto_create_rca}
    Auto group invite enabled:          {incident_auto_group_invite_enabled}
    Auto group invite group name:       {incident_auto_group_invite_group_name}
    Confluence API address:             {confluence_api_url}
    Confluence user:                    {confluence_api_username}
    Confluence space:                   {confluence_space}
    Confluence parent page:             {confluence_parent_page}
    PagerDuty Integration enabled:      {pagerduty_integration_enabled}
    PagerDuty API user:                 {pagerduty_api_username}
    React to create incident enabled:   {incident_auto_create_from_react_enabled}
    React emoji:                        {incident_auto_create_from_react_emoji_name}
    Statuspage integration enabled:     {statuspage_integration_enabled}
    Zoom Meeting Autocreate             {auto_create_zoom_meeting}
--------------------------------------------------------------------------------
    """
    if wrap:
        return f"""
```
{msg}
```
        """
    else:
        return msg
