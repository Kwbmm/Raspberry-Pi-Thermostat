#!/bin/bash
#
#These lines of code are taken from https://howto.biapy.com/en/debian-gnu-linux/servers/http/create-a-ssl-tls-certificate-on-debian
#Here we are creating an SSL certificate to be used with our Lighttpd server
#
#It is assumed openssl and ssl-cert packages are already installed

#Save the hostname into a variable
SSL_KEY_NAME="$(hostname --fqdn)"

#Create a temporary config file
CONF_FILE="$(mktemp)"
sed \
    -e "s/@HostName@/${SSL_KEY_NAME}/" \
    -e "s|privkey.pem|/etc/ssl/private/${SSL_KEY_NAME}.pem|" \
    '/usr/share/ssl-cert/ssleay.cnf' > "${CONF_FILE}"

sudo openssl req -config "${CONF_FILE}" -new -x509 -days 3650 -nodes -out "/etc/ssl/certs/${SSL_KEY_NAME}.crt" -keyout "/etc/ssl/private/${SSL_KEY_NAME}.key"
rm "${CONF_FILE}"

#Protect the private key
sudo chown root:ssl-cert "/etc/ssl/private/${SSL_KEY_NAME}.key"
sudo chmod 440 "/etc/ssl/private/${SSL_KEY_NAME}.key"

sudo make-ssl-cert '/usr/share/ssl-cert/ssleay.cnf' '/etc/ssl/certs/${SSL_KEY_NAME}.crt'