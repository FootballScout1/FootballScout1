#!/usr/bin/env bash
# sets up the web servers for the deployment of football scout static files

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install nginx
sudo mkdir -p /data/football_scout/releases/test /data/football_scout/shared
echo "This is a test" | sudo tee /data/football_scout/releases/test/index.html
sudo ln -sf /data/football_scout/releases/test/ /data/football_scout/current
sudo chown -hR ubuntu:ubuntu /data/
sudo sed -i '38i\\tlocation /football_scout_static/ {\n\t\talias /data/football_scout/current/;\n\t}\n' /etc/nginx/sites-available/default
sudo service nginx start

