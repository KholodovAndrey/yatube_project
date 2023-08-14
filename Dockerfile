FROM python:3.9-slim
COPY ./yatube/ .
RUN pip3 install -r ./requirements.txt --no-cache-dir
CMD ["gunicorn", "yatube.wsgi:application", "--bind", "0:8000" ]