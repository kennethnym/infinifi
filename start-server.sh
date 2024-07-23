#!/bin/sh
uvicorn server:app --host 0.0.0.0 --port 443 --ssl-keyfile private.key.pem --ssl-certfile domain.cert.pem > server.log 2> server.err < /dev/null
