FROM docker

RUN apk add --no-cache git python3 && \
    ln -s /usr/bin/python3 /usr/local/bin/python

WORKDIR /root

RUN git clone https://github.com/slackhq/python-rtmbot
WORKDIR python-rtmbot
RUN python3 -m pip install -r requirements.txt

RUN mkdir plugins/os_command_injection
COPY constant.py plugins/os_command_injection
COPY docker.py plugins/os_command_injection
COPY code_runner.py plugins/os_command_injection
COPY os_command_injection.py plugins/os_command_injection
COPY utils.py plugins/os_command_injection

RUN mkdir logs

COPY start.sh .

ENTRYPOINT ["sh", "-c"]
CMD ["./start.sh"]
