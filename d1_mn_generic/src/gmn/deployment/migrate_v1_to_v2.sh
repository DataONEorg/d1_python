#!/usr/bin/env bash

exec 2> /dev/null

export d1=/var/local/dataone

export v1b=${d1}/gmn/bin
export v2b=${d1}/gmn_venv/bin

export v1p=${d1}/gmn/lib/python2.7/site-packages
export v2p=${d1}/gmn_venv/lib/python2.7/site-packages

export v1h=${v1p}/service
export v2h=${v2p}/gmn

export v1s=${v1h}/settings_site.py
export v2s=${v2h}/settings_site.py


service apache2 stop

# settings_site.py

if [[ ! -f ${v1s} ]]; then
    echo "${v1s} does not exist. Aborting."
    exit
fi

cp ${v1s} ${v2s}

sed -ri "s/django.utils.log.NullHandler/logging.NullHandler/" ${v2s}

sed -ri "s/GMN_DEBUG/DEBUG_GMN/" ${v2s}
sed -ri "/DEBUG_GMN\s*=/a\DEBUG_PYCHARM = False" ${v2s}

sed -ri "s/^(PUBLIC_OBJECT_LIST\s*=).*/\1 True/" ${v2s}
sed -ri "s/^(PUBLIC_LOG_RECORDS\s*=).*/\1 True/" ${v2s}

sed -ri "s/'NAME':\s*'gmn'/'NAME': 'gmn2'/" ${v2s}

sed -ri "s/^(TIER\s*=)/# MIGRATE: \1/" ${v2s}
sed -ri "/TIER\s*=/a\# TIER setting removed in GMN v2. Replication is controlled with NODE_REPLICATE." ${v2s}

sed -ri "/^REQUIRE_WHITELIST_FOR_UPDATE\s*=/a\SLENDER_NODE = False" ${v2s}

sed -ri "s/^(MEDIA_ROOT\s*=)/# MIGRATE: \1/" ${v2s}

sed -ri "s/^(SYSMETA_STORE_PATH\s*=)/# MIGRATE: \1/" ${v2s}

sed -ri "s/^(OBJECT_STORE_PATH\s*=)/# MIGRATE: \1/" ${v2s}
sed -ri "/OBJECT_STORE_PATH\s*=/a\OBJECT_STORE_PATH = '/var/local/dataone/gmn_object_store'" ${v2s}

sed -ri "s/WRAPPED_MODE_BASIC_AUTH_ENABLED/PROXY_MODE_BASIC_AUTH_ENABLED/g" ${v2s}
sed -ri "s/WRAPPED_MODE_BASIC_AUTH_ENABLED/PROXY_MODE_BASIC_AUTH_ENABLED/g" ${v2s}
sed -ri "s/WRAPPED_MODE_BASIC_AUTH_USERNAME/PROXY_MODE_BASIC_AUTH_USERNAME/g" ${v2s}
sed -ri "s/WRAPPED_MODE_BASIC_AUTH_PASSWORD/PROXY_MODE_BASIC_AUTH_PASSWORD/g" ${v2s}
sed -ri "s/WRAPPED_MODE_STREAM_TIMEOUT/PROXY_MODE_STREAM_TIMEOUT/g" ${v2s}
sed -ri "/^PROXY_MODE_BASIC_AUTH_PASSWORD\s*=/a\PROXY_MODE_STREAM_TIMEOUT = 30" ${v2s}

# Apache

export as=/etc/apache2/sites-available
export ac=${as}/gmn2-ssl.conf

cp ${v2h}/deployment/gmn2-ssl.conf ${ac}

a2dissite gmn-ssl.conf
a2ensite gmn2-ssl.conf

# Postgres

sudo -u postgres dropdb gmn2
sudo -u postgres createdb gmn2 -E UTF8 gmn

# Django DB

sudo -u gmn ${v2b}/python ${v2h}/manage.py makemigrations
sudo -u gmn ${v2b}/python ${v2h}/manage.py migrate --run-syncdb

# Permissions

chown -R gmn:www-data ${d1}
chmod -R g+w ${d1}

# Start GMN v2

service apache2 start
