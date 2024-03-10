r"""
Evennia settings file.

The available options are found in the default settings file found
here:

/usr/src/evennia/evennia/settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *


######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "MyGame"
TIME_ZONE = "America/Chicago"
USE_TZ = True
IN_GAME_ERRORS = True
BROADCAST_SERVER_RESTART_MESSAGES = True
NEW_ACCOUNT_REGISTRATION_ENABLED = False

WEBSOCKET_CLIENT_URL="wss://evennia.lytle.pw:4002/"

CSRF_TRUSTED_ORIGINS = ['https://evennia.lytle.pw']


# Multiple characters per account, requires manual creation and login

MULTISESSION_MODE = 2
AUTO_CREATE_CHARACTER_WITH_ACCOUNT = False
AUTO_PUPPET_ON_LOGIN = False
MAX_NR_CHARACTERS = 5
DEBUG = False
# COMMAND_DEFAULT_CLASS = "commands.command.Command"

INSTALLED_APPS += ('web.chargen', 'web.character',
                   'django.contrib.humanize.apps.HumanizeConfig',
                   'django_nyt.apps.DjangoNytConfig',
                   'mptt',
                   'sorl.thumbnail',
                   'wiki.apps.WikiConfig',
                   'wiki.plugins.attachments.apps.AttachmentsConfig',
                   'wiki.plugins.notifications.apps.NotificationsConfig',
                   'wiki.plugins.images.apps.ImagesConfig',
                   'wiki.plugins.macros.apps.MacrosConfig',
                   )

# Disable wiki handling of login/signup, so that it uses your Evennia login system instead
WIKI_ACCOUNT_HANDLING = False
WIKI_ACCOUNT_SIGNUP_ALLOWED = False

# Enable wikilinks, e.g. [[Getting Started]]
WIKI_MARKDOWN_KWARGS = {
    'extensions': [
        'wikilinks',
    ]
}


# Custom methods to link wiki permissions to game perms
def is_superuser(article, user):
    """Return True if user is a superuser, False otherwise."""
    return not user.is_anonymous and user.is_superuser


def is_builder(article, user):
    """Return True if user is a builder, False otherwise."""
    return not user.is_anonymous and user.permissions.check("Builder")


def is_player(article, user):
    """Return True if user is a builder, False otherwise."""
    return not user.is_anonymous and user.permissions.check("Player")


# Create new users
WIKI_CAN_ADMIN = is_superuser

# Change the owner and group for an article
WIKI_CAN_ASSIGN = is_superuser

# Change the GROUP of an article, despite the name
WIKI_CAN_ASSIGN_OWNER = is_superuser

# Change read/write permissions on an article
WIKI_CAN_CHANGE_PERMISSIONS = is_superuser

# Mark an article as deleted
WIKI_CAN_DELETE = is_builder

# Lock or permanently delete an article
WIKI_CAN_MODERATE = is_superuser

# Create or edit any pages
WIKI_CAN_WRITE = is_builder

# Read any pages
WIKI_CAN_READ = is_player

# Completely disallow editing and article creation when not logged in
WIKI_ANONYMOUS_WRITE = False

CHARGEN_MENU = "world.chargen_menu"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "evennia",
        "USER": "evennia",
        "PASSWORD": "evennia1234",
        "HOST": "10.0.10.3",
        "PORT": "3306",
    }
}


######################################################################
# XYZ Grid install settings
######################################################################

# make contrib prototypes available as parents for map nodes
PROTOTYPE_MODULES += ['evennia.contrib.grid.xyzgrid.prototypes', 'world.items.gear.prototypes_gathering',
                      'world.items.gear.prototypes_crafting', 'world.items.gear.prototypes_tools',
                      'world.items.gear.prototypes_containers', 'world.items.furniture.pt_fountains',
                      'world.items.gear.prototypes_gear']

CRAFT_RECIPE_MODULES = ['world.characters.crafting.blacksmithing']

# add launcher command
EXTRA_LAUNCHER_COMMANDS['xyzgrid'] = 'evennia.contrib.grid.xyzgrid.launchcmd.xyzcommand'

# add game-specific maps
XYZGRID_MAP_LIST = ['world.maps.orario',]


######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
