# APT based install

This avoids dependencies on PyPI, which may result in a more secure deployment.

-

sudo apt update -y
sudo apt dist-upgrade -y

sudo apt install -y \
python3 \
python3-asn1crypto \
python3-cachecontrol \
python3-certifi \
python3-cffi \
python3-chardet \
python3-contextlib2 \
python3-cryptography \
python3-django \
python3-idna \
python3-iso8601 \
python3-isodate \
python3-lxml \
python3-msgpack \
python3-pkg-resources \
python3-psycopg2 \
python3-pyasn1 \
python3-pycparser \
python3-jwt \
python3-pyparsing \
python3-tz \
python3-pyxb \
python3-rdflib \
python3-requests-toolbelt \
python3-requests \
python3-six \
python3-urllib3 \
python3-zipstream

~~

# apt install python3-setuptools

~~

nano /usr/local/lib/python3.6/dist-packages/dataone.pth

/var/local/dataone/d1_python/lib_client/src
/var/local/dataone/d1_python/lib_common/src
/var/local/dataone/d1_python/gmn/src
/var/local/dataone/d1_python/lib_scimeta/src

~~

export GMN_PKG_DIR=/var/local/dataone/d1_python/gmn/src

~~

sudo -Hs

apt install --yes apache2 apache2-dev libapache2-mod-wsgi-py3

cp ${GMN_PKG_DIR}/d1_gmn/deployment/gmn2-ssl.conf /etc/apache2/sites-available
cp ${GMN_PKG_DIR}/d1_gmn/deployment/forward_http_to_https.conf /etc/apache2/conf-available
sed -Ei "s/(ServerName\s*).*/\1`hostname`/" /etc/apache2/sites-available/gmn2-ssl.conf

a2enmod --quiet wsgi ssl rewrite
a2enconf --quiet forward_http_to_https
a2ensite --quiet gmn2-ssl

~~~

apt install --yes postgresql
passwd -d postgres
su postgres -c passwd

su postgres -c 'createuser gmn'
su postgres -c 'createdb -E UTF8 gmn2'

~~~

mkdir -p /var/local/dataone/certs/local_ca/{certs,newcerts,private}
cd /var/local/dataone/certs/local_ca
cp ${GMN_PKG_DIR}/d1_gmn/deployment/openssl.cnf .
touch index.txt

openssl req -config ./openssl.cnf -new -newkey rsa:2048 \
-keyout private/ca_key.pem -out ca_csr.pem

openssl ca -config ./openssl.cnf -create_serial \
-keyfile private/ca_key.pem -selfsign -extensions v3_ca_has_san \
-out ca_cert.pem -infiles ca_csr.pem

cd /var/local/dataone/certs/local_ca

openssl req -config ./openssl.cnf -new -newkey rsa:2048 -nodes \
-keyout private/client_key.pem -out client_csr.pem

~~~

Install non trusted certs here.

cd /var/local/dataone/certs/local_ca
mkdir -p ../ca
cp ca_cert.pem ../ca/local_ca.pem
sudo c_rehash ../ca

~~~

cp ${GMN_PKG_DIR}/d1_gmn/settings_template.py ${GMN_PKG_DIR}/d1_gmn/settings.py

~~~

chown -R gmn:www-data /var/local/dataone/
chmod -R g+w /var/local/dataone/
timedatectl set-timezone Etc/UTC
ufw allow 443

~~~

python3 ${GMN_PKG_DIR}/d1_gmn/manage.py migrate --run-syncdb

~~~

settings.py:

MIDDLEWARE_CLASSES -> MIDDLEWARE

~~~

new pattern to use in doc rst:

sudo -Hs sh -c '
echo $HOME;
echo another;
whoami;
ls /;
'

~~
