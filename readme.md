sudo journalctl -u shopsepid.service

sudo systemctl restart shopsepid.service

sudo systemctl status shopsepid.service

source /var/www/shopsepid/venv/bin/activate


journalctl -u shopsepid.service -n 100
journalctl -u shopsepid.service -f


python3 manage.py collectstatic