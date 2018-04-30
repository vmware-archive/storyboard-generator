
FROM node:8

COPY ui /ui

WORKDIR /ui

#ADD docker-npm-proxy /ui/.npmrc
RUN yarn --verbose
RUN yarn build -- --prod --aot

RUN find /ui/dist


# Build the package
FROM python:3

ADD storyboardgenerator/setup.py /storyboardpackage/
ADD storyboardgenerator/storyboardgenerator/*.py /storyboardpackage/storyboardgenerator/
ADD storyboardgenerator/setup.py /storyboardpackage/
WORKDIR /storyboardpackage

RUN find /storyboardpackage
RUN python setup.py sdist -v --keep-temp
RUN find /storyboardpackage/dist && tar -ztf /storyboardpackage/dist/storyboardgenerator-*.tar.gz

# Run the server!
FROM python:3
ADD flask/app.py /flaskserver/
ADD flask/settings-docker.conf /flaskserver/settings.conf

COPY assets /assets
COPY --from=0 /ui/dist /ui
COPY --from=1 /storyboardpackage/dist/storyboardgenerator-*.tar.gz /storyboardgenerator.tar.gz

RUN pip install Flask==0.12.2
RUN pip install /storyboardgenerator.tar.gz

ENV FLASK_APP=/flaskserver/app.py
ENV ASSETS_SETTINGS=settings.conf


CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]

EXPOSE 5000 80
