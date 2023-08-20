FROM python:3.10.10-bullseye AS base
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get -f install -y linux-libc-dev
WORKDIR /source
COPY requirements.txt .

#ajustes sonar
RUN pip install --upgrade pip
RUN pip uninstall -y setuptools
RUN pip uninstall -y wheel 
RUN pip install setuptools>=65.5.1
RUN pip install wheel>=0.38.1

RUN pip install --no-cache-dir -r requirements.txt
COPY . ./redacai-api
EXPOSE 8080
ENTRYPOINT ["uvicorn", "redacai-api.main:app", "--port", "8080", "--host", "0.0.0.0"]

FROM base AS final