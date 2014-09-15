Aquila_microblog
================

This is a micro blog -- "Aquila".

1. create virtualenv

	\> cd Aquila_microblog

	\> virtualenv venv

2. activate virtualenv

	in Linux:
	
	$ . venv/bin/activate

	in Windows:

	venv\scripts> activate

3. install Flask in venv

	\> pip install Flask

4. Initial db in Python Shell:

	\>>> from flaskr import init_db

	\>>> init_db()

5. run microblog

	Aquila_microblog> python microblog.py
