FROM blurrcat/alpine-python-psycopg2:1.0 as base
ENV PYTHONUNBUFFERED 1
WORKDIR /opt/cryptonite
RUN apk add --no-cache bash postgresql-client
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN adduser -D cryptonite
USER cryptonite
ENTRYPOINT ["./entrypoint.sh"]