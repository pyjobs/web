APP_CONFIG = "/srv/www/pyjobs.dev.algoo.fr/pyjobs_web/development.ini"

#Setup logging
# import logging
# logging.config.fileConfig(APP_CONFIG)

#Load the application
from paste.deploy import loadapp
application = loadapp('config:%s' % APP_CONFIG)
application.debug = False
