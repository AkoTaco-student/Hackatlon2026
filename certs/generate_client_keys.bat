@echo off
REM Batch file equivalent of generate_client_keys.sh

if "%1"=="" (
    echo must provide name as an argument
    exit /b 1
)

set NAME=%1

mkdir %NAME%
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-384 -out %NAME%\client%NAME%_private.pem

openssl req -new -key %NAME%\client%NAME%_private.pem -out %NAME%\client%NAME%_cert.csr -subj "/C=NO/CN=HacatlonClient%NAME%/O=NTNU"

openssl x509 -req -in %NAME%\client%NAME%_cert.csr -CA ec_ca_cert.pem -CAkey ec_ca_private.pem -extfile x509.ext -extensions client -days 3650 -sha256 -out %NAME%\client%NAME%_cert.pem

type %NAME%\client%NAME%_cert.pem > %NAME%\client%NAME%_certs.crt
copy ca_certs.crt %NAME%\
