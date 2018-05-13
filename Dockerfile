FROM docker

RUN apk add --no-cache git python3 && \
    ln -s /usr/bin/python3 /usr/local/bin/python

WORKDIR /root

# ADD https://api.github.com/repos/odanado/slackbot-os-command-injection/git/refs/heads/master version.json
# RUN git clone https://github.com/odanado/slackbot-os-command-injection
ADD . slackbot-os-command-injection

WORKDIR slackbot-os-command-injection

RUN python3 -m pip install -r requirements.txt

RUN mkdir -p logs
ENV DEBIAN_FRONTEND=noninteractive
CMD ["./start.sh"]
