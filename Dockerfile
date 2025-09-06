FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /main

COPY requirements.txt /main/requirements.txt
RUN pip install --no-cache-dir -r /main/requirements.txt

COPY src/ /main/src/
COPY scripts/ /main/scripts/

ENV PYTHONPATH=/main

CMD ["-c", "bash", "/main/scripts/prestart.sh"]
