FROM python:3.5-stretch AS build-env
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

FROM gcr.io/distroless/python3
COPY --from=build-env /app /app
COPY --from=build-env /usr/local/lib/python3.5/site-packages /usr/local/lib/python3.5/site-packages
WORKDIR /app
ENV APP_SETTINGS="config.TestingConfig"
ENV DATABASE_URL="postgresql://localhost/caissenoire"
ENV PYTHONPATH=/usr/local/lib/python3.5/site-packages
EXPOSE 8000
CMD ["app.py"]
