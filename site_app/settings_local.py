"""Local setings module

This module used for storing environment-specified settings
"""

DEBUG = True

# Mailing
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'admin@bookmarks.ru'

# test mailing server
_run_smtp = 'python -m smtpd -n -c DebuggingServer localhost:1025'
print('For view email, please run this command: ' + _run_smtp)

