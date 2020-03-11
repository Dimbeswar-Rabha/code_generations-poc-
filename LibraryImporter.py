class Import:
    def __init__(self, file_name):
        self.file_name = file_name

    def import_library(self):
        if self.file_name in ['test_mqtt_subscriber_origin.py', 'test_mqtt_publisher_destination.py']:
            line = ('import pytest\n'
                    'import time\n'
                    '\n'
                    'from streamsets.testframework.decorators import stub\n'
                    'from streamsets.testframework.markers import mqtt')
        elif self.file_name == 'test_influxdb_destination.py':
            line = ('import json\n'
                    'import logging\n'
                    'import pytest\n'
                    'import string\n'
                    '\n'
                    'from streamsets.testframework.decorators import stub\n'
                    'from streamsets.testframework.markers import influxdb\n'
                    'from streamsets.testframework.utils import get_random_string\n'
                    '\n'
                    'logger = logging.getLogger(__name__)'
                    )

        elif self.file_name == 'test_mongodb_origin.py':
            line = ('import copy\n'
                    'import logging\n'
                    'import pytest\n'
                    'import time\n'
                    '\n'
                    'from streamsets.testframework.decorators import stub\n'
                    'from streamsets.testframework.markers import mongodb, sdc_min_version\n'
                    'from streamsets.testframework.utils import get_random_string\n\n'
                    'logger = logging.getLogger(__name__)')
        return line



