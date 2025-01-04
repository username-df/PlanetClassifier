FROM python:3.10-slim AS build

WORKDIR /flaskapp
ADD . /flaskapp
RUN pip install --no-cache-dir -r requirements.txt

FROM python:alpine AS final

WORKDIR /flaskapp
COPY --from=build /flaskapp/ /flaskapp/
EXPOSE 8080
CMD ["python", "./app.py"]