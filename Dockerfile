FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN python --version
RUN pip3 --version

RUN pip3 install torch==2.1.0 -f https://download.pytorch.org/whl/cu111/torch_stable.html && \
	pip3 install setuptools wheel && \
  pip3 install --no-cache-dir -r /code/requirements.txt -f https://download.pytorch.org/whl/cu111/torch_stable.html

COPY . /code

CMD ["fastapi", "run", "server.py", "--port", "8000"]

