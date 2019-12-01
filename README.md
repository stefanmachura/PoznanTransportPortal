# PoznanTransportPortal

Web portal that allows the user to check the timetable of a bus or tramstop. Together with the timetable, the user is presented with the nearest bike stations of the Poznań Bike System.

To install the application:

clone the project
create a Python virtual env
pip install -r requirements.txt
python manage.py migrate
python manage.py populate_stops (to create/update the stops db)
python manage.py runserver
