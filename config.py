# -*- coding: utf-8 -*-
# VK config
from os import getcwd, makedirs, environ
from os.path import join as path_join

config = {
    # SQL database config
    'DB_USER': environ.get('DB_USER', 'user'),
    'DB_PASSWORD': environ.get('DB_PASSWORD', ''),
    'DB_HOST': environ.get('DB_HOST', 'localhost'),
    'DB_NAME': environ.get('DB_NAME', 'db_sample'),
    'DB_PORT': environ.get('DB_PORT', '3306'),  # default mysql port

    # Telegram config
    'TELEGRAM_TOKEN': environ.get('TELEGRAM_TOKEN', ''),  # get it from https://t.me/botfather

    # Imgur config
    'IMGUR_CLIENT_ID': environ.get('IMGUR_CLIENT_ID', ''),
    'IMGUR_CLIENT_SECRET': environ.get('IMGUR_CLIENT_SECRET', ''),
    'IMGUR_ALBUM_ID': environ.get('IMGUR_ALBUM_ID', ''),
    'IMGUR_REFRESH_TOKEN': environ.get('IMGUR_REFRESH_TOKEN', ''),

    'OWNER_ID': int(environ.get('OWNER_ID', '0')),  # bot owner telegram id

    'LOG_FILE': environ.get('LOG_FILE', 'squik.log'),

    # Flask config
    'EXTERNAL_HOST': environ.get('EXTERNAL_HOST', 'host.name'),
    'EXTERNAL_PORT': int(environ.get('EXTERNAL_PORT', '8443')),  # 80/443/88/8443
    'WEBHOOK_LISTEN': environ.get('WEBHOOK_LISTEN', '0.0.0.0'),
    'INTERNAL_PORT': int(environ.get('INTERNAL_PORT', '1234')),

    'WEBHOOK_URL': environ.get('WEBHOOK_URL', 'https://localhost/'),

    'USE_CERT_FILE': bool(environ.get('USE_CERT_FILE', '0')),

    'ERROR_LOGS_DIR': path_join(getcwd(), 'errlogs', '')}
makedirs(config['ERROR_LOGS_DIR'], exist_ok=True)

if config['USE_CERT_FILE']:
    # Generate SSL certificate with "openssl genrsa -out webhook_pkey.pem 2048"
    config['WEBHOOK_SSL_CERT'] = path_join(getcwd(), environ.get('WEBHOOK_SSL_CERT', 'webhook_cert.pem'))
    # Generate private key with "openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem"
    config['WEBHOOK_SSL_PRIV'] = path_join(getcwd(), environ.get('WEBHOOK_SSL_PRIV', 'webhook_pkey.pem'))

REQUESTS_PROXY = {}
