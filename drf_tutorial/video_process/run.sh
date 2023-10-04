rm -r video_process/media/*/
mkdir video_process/media
python manage.py flush
python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
python manage.py runserver 127.0.0.1:8000
