APP_CONFIG = "/srv/www/pyjobs.fr/pyjobs_web/production.ini"

#Setup logging
# import logging
# logging.config.fileConfig(APP_CONFIG)

#Load the application
from paste.deploy import loadapp
application = loadapp('config:%s' % APP_CONFIG)
application.debug = False
