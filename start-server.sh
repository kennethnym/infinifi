#!/bin/sh
INFERENCE_SERVER_URL=SERVER_URL API_KEY=FAL_API_KEY nohup uvicorn server:app --host 0.0.0.0 --port 443 --ssl-keyfile /path/to/ssl/private/key/file --ssl-certfile /path/to/ssl/cert/file > server.log 2> server.err < /dev/null &
