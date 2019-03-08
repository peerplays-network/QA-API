FROM ubuntu:16.04
MAINTAINER PeerPlays Blockchain Standards Association

RUN \
    apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-dev python3-pip libmysqlclient-dev libssl-dev git && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create app directory
RUN mkdir /app
ADD requirements.txt /app

# Install app requirements
RUN pip3 install -r /app/requirements.txt
RUN pip3 install peerplays --upgrade
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN peerplays set node <> # your desired API node
RUN peerplays createwallet --password <> # your desired password
RUN echo supersecret | peerplays addkey <># key for your Peerplays account
RUN peerplays set default_account <> # account name

# Install app
ADD . /app

# Make settings persistent
VOLUME ["/app"]

# rpc service:
EXPOSE 5050

# default execute entry
WORKDIR /app
CMD echo <> | python3 -u /app/qaapi.py #replace <> with your peerplays python wallet password
