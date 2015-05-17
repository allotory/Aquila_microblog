# Aquila Microblog

## What is Aquila Microblog?

Aquila Microblog is a decently featured microblogging web application written in Python and Flask.

## Features

* Post blog.
* Following people.
* Add friends.
* Send and receive message.
* and _much_ more!

## Installation for Development

* create virtualenv

	    > cd Aquila_microblog
	    
	    > virtualenv venv

2. activate virtualenv
    
    in Linux:
    	
    	$ . venv/bin/activate
    
    in Windows:
    
    	venv\scripts> activate

3. install Flask in venv

		> pip install Flask

4. Initial db in Python Shell:

		>>> from microblog import init_db
	
		>>> init_db()

5. run microblog

		Aquila_microblog> python microblog.py

## Contributing

Pull requests are being accepted! If you would like to contribute, simply fork
the project and make your changes.

##Support:

Support now is given by me.

## License

The GPL License


