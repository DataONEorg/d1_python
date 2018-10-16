#!/usr/bin/env bash

set -x
set -d

d1=/var/local/dataone

v1v=${d1}/gmn
v2v=${d1}/gmn_venv

v1b=${v1v}/bin
v2b=${v2v}/bin

v1p=${d1}/gmn/lib/python2.7/site-packages
v2p=${d1}/gmn_venv/lib/python2.7/site-packages

v1h=${v1p}/service
v2h=${v2p}/d1_gmn

v1s=${v1h}/settings_site.py
v2s=${v2h}/settings_site.py

for f in "${d1}" "${v1b}" "${v2b}" "${v1s}"; do
    if [ ! -e "$f" ]; then
        echo "$f does not exist. Aborting." >&2;
        exit 1;
    fi
done

exec 2> /dev/null

service apache2 stop

# settings_site.py

cp ${v1s} ${v2s}

sed -ri "s/django.utils.log.NullHandler/logging.NullHandler/" ${v2s}

sed -ri "s/GMN_DEBUG/DEBUG_GMN/" ${v2s}

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

sed -ri "s/WRAPPED_MODE/PROXY_MODE/g" ${v2s}
sed -ri "/^PROXY_MODE_BASIC_AUTH_PASSWORD\s*=/a\PROXY_MODE_STREAM_TIMEOUT = 30" ${v2s}

# Apache

as=/etc/apache2/sites-available
a1c=${as}/gmn-ssl.conf
a2c=${as}/gmn2-ssl.conf

cp ${a1c} ${a2c}

sed -ri "s/(.*WSGIPythonHome).*/\1 ${v2v////\\/}/I" ${a2c}
sed -ri "s/(.*WSGIScriptAlias).*/\1 \/mn ${v2h////\\/}\/wsgi.py/I" ${a2c}
sed -ri "s/(.*WSGIDaemonProcess).*/\1 gmn2 user=gmn processes=2 threads=25 python-path=${d1////\\/}:${v2p////\\/}/I" ${a2c}
sed -ri "s/(.*)<FilesMatch.*/\1<Files \"wsgi.py\">/I" ${a2c}
sed -ri "s/(.*)<\/FilesMatch.*/\1<\/Files>/I" ${a2c}
sed -ri "s/(.*WSGIProcessGroup).*/\1 gmn2/I" ${a2c}
sed -ri "s/(.*<Directory).*service.*/\1 ${v2h////\\/}>/I" ${a2c}
sed -ri "s/(.*Alias\s\/robots\.txt).*/\1 ${v2h////\\/}\/app\/static\/robots.txt/I" ${a2c}
sed -ri "s/(.*Alias\s\/static\/).*/\1 ${v2h////\\/}\/app\/static\//I" ${a2c}

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
