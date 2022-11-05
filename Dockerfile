FROM python:3.9

ENV PYTHONPATH=/code/pyxor

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./pyxor /code/pyxor
COPY ./scripts/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["server"]