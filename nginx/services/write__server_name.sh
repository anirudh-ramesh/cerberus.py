#!/bin/sh

# /etc/nginx/conf.d/

for file in *.conf.template; do
	envsubst '\${SUBDOMAIN_SUFFIX} \${DOMAIN_NAME}' < ${file} > $1${file%.*}
done
