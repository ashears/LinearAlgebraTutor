# CIS 422
# Project 2: Linear Algebra Visualizer
#
# By: Andrew Cvitanovich, Ashton Shears, Adrian Scheuerell and Marc Lee

# commands to activate python3 virtual environment and setup flask debugging environment
INVENV = . env/bin/activate ; export FLASK_DEBUG=0 ;

# run the flask server
run: install
	($(INVENV) python3 src/main.py)&

# install the site's flask based server
install:
	python3 -m venv env
	# this is here to fix a bug with mpld3 when it tries to plot scatter plots
	#pip3 install --user "git+https://github.com/javadba/mpld3@display_fix"
	$(INVENV) pip3 install -r requirements.txt

# updates the reqirements
dist:	env
	$(INVENV) pip freeze > requirements.txt

# removes compiled and installed code
clean:
	rm -f *.pyc */*.pyc
	rm -rf __pycache__ */__pycache__
	rm -rf env
	rm -rf .DS_Store
	rm -rf src/.DS_Store
