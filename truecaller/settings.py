import os
from distutils.util import strtobool

from django.core.exceptions import ImproperlyConfigured
from django.core.management.utils import get_random_secret_key


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.getenv(name)
        try:
            return bool(strtobool(value))
        except ValueError as e:
            error_msg = "{} is an invalid value for {}".format(value, name)
            raise ImproperlyConfigured(error_msg) from e
    return default_value


DEBUG = get_bool_from_env("DEBUG", True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def generate_secret_key(filename):
    f = open(filename, "w")
    f.write(f"SECRET_KEY='{get_random_secret_key()}'")
    f.close()


try:
    from secret_key import SECRET_KEY
except ImportError:
    generate_secret_key(os.path.join(BASE_DIR, "secret_key.py"))
    from secret_key import SECRET_KEY  # noqa


def get_env_variable_or_default(name, default_value):
    if name in os.environ:
        return os.getenv(name)
    else:
        if type(default_value) == "int":
            return int(default_value)
        else:
            return default_value


def get_env_variable(var_name):
    try:
        return os.getenv(var_name)
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main_app",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_swagger",
    "drf_yasg",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"  # <-- And here
    ]
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "truecaller.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "truecaller.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},  # noqa
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},  # noqa
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },  # noqa
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"
