virtualenv -p `which python2` --no-site-packages .
source bin/activate
pip install -r requirements.txt
export DATABASE_URL="sqlite:///database.sqlite"
python2 manage.py syncdb -v 3
python2 manage.py migrate
python2 manage.py runserver
