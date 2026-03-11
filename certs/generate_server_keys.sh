
#note ed448 is not fips compatible (FIPS is american standard) so we use standard elliptic crypto P-384 curve and not RSA. 
# Those are supported by NSM


#step 1
#ca key generation is now disabled, enable only if ca keys shall be re-generated
# enable following 5 lines if you would like to re-generate certificate authority private key and certificate. 
#In that case all of client keys will be invalid and shall be updated
#openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-384 -out ec_ca_private.pem
#openssl req -x509 -new -key ec_ca_private.pem -out ec_ca_cert.pem -days 3650 -sha256 -subj "/C=NO/CN=HackatlonCA/O=NTNU" -addext "keyUsage=critical,cRLSign,keyCertSign,digitalSignature"
#mkdir -p ca_dir
#cp ec_ca_private.pem ca_dir/
#cp ec_ca_cert.pem    ca_dir/

#step 2
#we do not use issuer certificate in a chain, so this is also commented out, to simplifiy the solution
#openssl req -new -key ec_issuer_private.pem -out ec_issuer_cert.csr -subj "/C=NO/CN=HackatlonIssuer/O=NTNU"

#openssl x509 -req -in ed448_issuer_cert.csr -CA ed448_mqttca_cert.pem -CAkey ed448_ca_private.pem -extfile x509.ext -extensions issuer -days 3650 -sha256 -out ed448_mqttissuer_cert.pem

#step 3
#generate server private key
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-384 -out ec_server_private.pem
openssl req -new -key ec_server_private.pem -out ec_server_cert.csr -subj "/C=NO/CN=HackatlonServer/O=NTNU"

openssl x509 -req -in ec_server_cert.csr -CA ec_ca_cert.pem -CAkey ec_ca_private.pem -extfile x509.ext -extensions server -days 3650 -sha256 -out ec_server_cert.pem

#step 4, copy data into folders
cat  ec_server_cert.pem > server_certs.pem
cat  ec_ca_cert.pem > server_certs.crt

mkdir -p server_dir
cp server_certs.pem server_dir/
cp ec_server_cert.pem server_dir/
cp ec_server_private.pem server_dir/



