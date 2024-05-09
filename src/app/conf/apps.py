DEFAULT_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)
DEPENDENCIES = ("rest_framework", "rest_framework_simplejwt")
MODULES = (
    "chat",
    "account",
)
INSTALLED_APPS = MODULES + DEPENDENCIES + DEFAULT_APPS
