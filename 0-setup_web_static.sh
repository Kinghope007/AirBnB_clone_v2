#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

# check if Nginx is installed, and if not, install it
if ! dpkg -l | grep -q nginx; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/

# Create a fake HTML file for testing
echo "Fake content for testing" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create the symbolic link pointing to /data/web_static/releases/test/
sudo ln -sfn /data/web_static/releases/test/ /data/web_static/current

# Give ownership to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-enabled/default"
config_alias="server_name _;\n\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}"

# Add alias to Nginx config if not already present
if ! grep -q "$config_alias" "$config_file"; then
    sudo sed -i "s#server_name _;#$config_alias#" "$config_file"
fi

# Restart Nginx
sudo service nginx restart
