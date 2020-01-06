import os

class DevelopmentConfig():
    # Uses a hidden environment variable, can also use a string but only during development.
    # After dev this MUST be removed.

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hardcoded_string'
    # These are in a seperate area to help prevent Cross-site request forgery

class LiveConfig():
    # Uses a hidden environment variable, can also use a string but only during development.
    # After dev this MUST be removed.

    SECRET_KEY = os.environ.get('SECRET_KEY')
    # These are in a seperate area to help prevent Cross-site request forgery