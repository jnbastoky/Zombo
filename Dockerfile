FROM debian:testing

RUN apt update
RUN apt install -y hugo

EXPOSE 1313

