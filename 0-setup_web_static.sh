#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static.

# Install Nginx not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create fake HTML page
printf %s "<html>
  <head>
  </head>
  <body>
    Welcome!!!
  </body>
</html>
" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Ensure correct permissions on directories
sudo chown -R ubuntu:ubuntu /data/

# Configure Nginx to serve content of /data/web_static/current/ to hbnb_static
printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    # Custom header
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    # Serve content to /hbnb_static
    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html index.htm;
    }

    # Sets redirect_me to '301 Moved Permanently'
    location /redirect_me {
        return 301 https://youtube.com/;
    }

    # Custom 404 error page
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
