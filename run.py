# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# use >>flask run --host=0.0.0.0 --port=80 to run on the net
from apps import app

app.logger.info('DEBUG       = ' + str( app.config['DEBUG'] ))
app.logger.info('ASSETS_ROOT = ' + app.config['ASSETS_ROOT'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80')
