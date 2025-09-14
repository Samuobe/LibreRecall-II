
sudo mkdir /usr/bin/LibreRecall
sudo cp -r * /usr/bin/LibreRecall

sudo chmod 777 -R /usr/bin/LibreRecall

sudo cp LibreRecall_daemon.desktop /home/samuobe/.config/autostart/LibreRecall_daemon.desktop

cp LibreRecall.desktop /home/samuobe/.local/share/applications/LibreRecall.desktop

sudo cp icon.png /usr/share/pixmaps/LibreRecall.png