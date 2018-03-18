FROM odanado/os-command-injection:base

RUN apt update && apt upgrade -y
RUN apt install -y vim-common wget

RUN cd /tmp && \
    wget -nv https://raw.githubusercontent.com/fumiyas/home-commands/master/echo-sd && \
    install -m 0755 echo-sd /usr/local/bin/echo-sd && \
    rm echo-sd

RUN apt install -y bc dc zsh w3m curl git nkf software-properties-common

RUN apt-add-repository ppa:brightbox/ruby-ng && \
    apt update && \
    apt install -y ruby2.5

RUN gem install cureutils
