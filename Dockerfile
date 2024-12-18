FROM python:3.10-slim-buster
WORKDIR "/code"
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV DB_HOST=postgres
ENV DB_NAME=postgres
ENV DB_PASSWORD=postgres
ENV DB_PORT=5432
ENV DB_USER=postgres
ENV SETUP=true
COPY . .
RUN apt-get update
RUN pip install -r requirements.txt

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1

EXPOSE 5000

CMD ["flask", "run", "--debug"]