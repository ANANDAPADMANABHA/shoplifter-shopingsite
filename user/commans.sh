server {
    listen 80;
    server_name 3.7.253.222;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root/home/ubuntu/project/shoplifter;
;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}