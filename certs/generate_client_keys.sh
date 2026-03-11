#!/bin/bash

if [ -z "$1" ]; then
   echo "must provide name as an argument";
   exit 1;
fi;

mkdir -p ./${1}
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-384 -out ./${1}/client${1}_private.pem

openssl req -new -key ./${1}/client${1}_private.pem -out ./${1}/client${1}_cert.csr -subj "/C=NO/CN=HacatlonClient${1}/O=NTNU"

openssl x509 -req -in ./${1}/client${1}_cert.csr -CA ec_ca_cert.pem -CAkey ec_ca_private.pem \
-extfile x509.ext -extensions client -days 3650  -sha256 -out ./${1}/client${1}_cert.pem

cat ./${1}/client${1}_cert.pem > ./${1}/client${1}_certs.crt
cp ca_certs.crt  ./${1}
