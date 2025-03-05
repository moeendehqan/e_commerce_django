sudo journalctl -u shopsepid.service

sudo systemctl restart shopsepid.service

sudo systemctl status shopsepid.service

source /var/www/shopsepid/venv/bin/activate


journalctl -u shopsepid.service -n 100


python3 manage.py collectstatic