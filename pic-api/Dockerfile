FROM python:3.13.4-slim-bullseye

ENV FLASK_PORT="5000"

COPY ./src ./

COPY ./.env ./

COPY ./requirements.txt ./

RUN sed -i "s|PLACHOLDER_AWS_ACCESS_KEY_ID|GITHUB_ACTIONS_ACCESS_ID_SECRET|g" /.env

RUN sed -i "s|PLACHOLDER_AWS_SECRET_ACCESS_KEY|GITHUB_ACTIONS_SECRET_KEY_SECRET|g" /.env

RUN pip install -r requirements.txt

EXPOSE ${FLASK_PORT}

CMD python3 ./main.py -p ${FLASK_PORT}
