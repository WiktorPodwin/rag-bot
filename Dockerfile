FROM python:3.12

WORKDIR /main

COPY requirements.txt /main/requirements.txt
RUN pip install --no-cache-dir -r /main/requirements.txt

# ENV PYTHONPATH=/main/src

COPY .src/ /main/src/

COPY .scripts/ /main/scripts/

RUN chmod +x /main/src/app/scripts/prestart.sh

RUN /main/src/app/scripts/prestart.sh
