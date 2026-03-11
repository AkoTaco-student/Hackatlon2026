@echo off
REM Batch file equivalent of generate_server_keys.sh
REM Note: ed448 is not FIPS compatible (FIPS is American standard) so we use standard elliptic crypto P-384 curve and not RSA.
REM Those are supported by NSM

REM step 1
REM ca key generation is now disabled, enable only if ca keys shall be re-generated
REM enable following 5 lines if you would like to re-generate certificate authority private key and certificate.
REM In that case all of client keys will be invalid and shall be updated
REM openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-384 -out ec_ca_private.pem
REM openssl req -x509 -new -key ec_ca_private.pem -out ec_ca_cert.pem -days 3650 -sha256 -subj "/C=NO/CN=HackatlonCA/O=NTNU" -addext "keyUsage=critical,cRLSign,keyCertSign,digitalSignature"
REM mkdir ca_dir
REM copy ec_ca_private.pem ca_dir\
REM copy ec_ca_cert.pem ca_dir\

REM step 2
REM we do not use issuer certificate in a chain, so this is also commented out, to simplifiy the solution
REM openssl req -new -key ec_issuer_private.pem -out ec_issuer_cert.csr -subj "/C=NO/CN=HackatlonIssuer/O=NTNU"
REM openssl x509 -req -in ed448_issuer_cert.csr -CA ed448_mqttca_cert.pem -CAkey ed448_ca_private.pem -extfile x509.ext -extensions issuer -days 3650 -sha256 -out ed448_mqttissuer_cert.pem

REM step 3
REM generate server private key
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-384 -out ec_server_private.pem
openssl req -new -key ec_server_private.pem -out ec_server_cert.csr -subj "/C=NO/CN=HackatlonServer/O=NTNU"

openssl x509 -req -in ec_server_cert.csr -CA ec_ca_cert.pem -CAkey ec_ca_private.pem -extfile x509.ext -extensions server -days 3650 -sha256 -out ec_server_cert.pem

REM step 4, copy data into folders
type ec_server_cert.pem > server_certs.pem
type ec_ca_cert.pem > server_certs.crt

mkdir server_dir
copy server_certs.pem server_dir\
copy ec_server_cert.pem server_dir\
copy ec_server_private.pem server_dir\
