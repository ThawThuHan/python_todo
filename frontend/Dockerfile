FROM nginx

ENV BACKEND_URL="http://192.168.10.120:5000"

WORKDIR /usr/share/nginx/html/

COPY . .

EXPOSE 80

CMD sed -i "s|http://127.0.0.1:5000|${BACKEND_URL}|g" /usr/share/nginx/html/script.js && nginx -g "daemon off;"