FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache shadow
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g $GROUP_ID appgroup && \
    useradd -m -u $USER_ID -g appgroup appuser


COPY config.py /app/
COPY main.py /app/
COPY crud.py /app/

RUN chown -R appuser:appgroup /app
USER appuser

ENV PORT=4000

EXPOSE ${PORT}
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]