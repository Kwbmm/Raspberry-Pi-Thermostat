#!/bin/bash
#
#This script should take care of setting up LightTPD to handle HTTPS
#Procedure is taken from https://howto.biapy.com/en/debian-gnu-linux/servers/http/install-and-setup-lighttpd-on-debian


SSL_KEY_NAME="$(hostname --fqdn)"

#Merge the SSL certificate private and public keys in the file /etc/lighttpd/server.pem
sudo cp '/etc/ssl/private/${SSL_KEY_NAME}.key' '/etc/lighttpd/server.pem'
sudo cat '/etc/ssl/certs/${SSL_KEY_NAME}.crt' >> '/etc/lighttpd/server.pem'

#Protect the access to server.pem
sudo chown root:root /etc/lighttpd/server.pem
sudo chmod go-rw /etc/lighttpd/server.pem

#Update the LigHTTPd configuration to make use of ca-certs.pem
sudo echo '$SERVER["socket"] == "0.0.0.0:443" {
  ssl.engine  = "enable"
  ssl.pemfile = "/etc/lighttpd/server.pem"
  ssl.ca-file = "/etc/lighttpd/ca-certs.pem"
}' > /etc/lighttpd/conf-available/10-ssl-with-ca.conf

#Enable the Lighttpd SSL module (use the "ssl" module if your certificate does not use a intermediate certificate)
sudo lighty-enable-mod ssl

#Reload LightTPD
sudo /etc/init.d/lighttpd force-reload