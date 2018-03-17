FROM odanado/os-command-injection:base

RUN apt install -y vim-common wget

RUN cd /tmp && \
    wget -nv https://raw.githubusercontent.com/fumiyas/home-commands/master/echo-sd && \
    install -m 0755 echo-sd /usr/local/bin/echo-sd && \
    rm echo-sd
