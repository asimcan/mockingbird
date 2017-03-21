FROM ubuntu:16.04

# Install.
RUN \
  apt-get install -y nginx && \
  rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/mockingbird/
ADD . /opt/mockingbird/

ADD nginx.conf /etc/nginx/nginx.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

ADD mockingbird-nginx-https.conf /etc/nginx/conf.d/
ADD mockingbird-nginx-http.conf /etc/nginx/conf.d/

RUN /env/bin/pip install -r /opt/mockingbird/requirements.txt

WORKDIR /opt/mockingbird

CMD ["/bin/bash", "start.sh"]

EXPOSE 80
EXPOSE 443

