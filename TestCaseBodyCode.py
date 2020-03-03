
class Body_code:
    def __init__(self, file_name,function):
        self.file_name = file_name
        self.line = function

    def get_body_code(self):
        if self.file_name == 'test_mqtt_subscriber_origin.py':
            stage_attributes = ', **stage_attributes' if 'stage_attributes' in self.line else ""
            line = f"""{self.line[0:len(self.line)-3]}, mqtt_broker):
    data_topic = 'mqtt_subscriber_topic'
    try:
        mqtt_broker.initialize(initial_topics=[data_topic])
        pipeline, mqtt_source = get_mqtt_trash_pipeline_and_mqtt_stage(sdc_builder, mqtt_broker{stage_attributes})
        #want to set attribute after configure for environment? set here.
        sdc_executor.add_pipeline(pipeline)
        running_snapshot = sdc_executor.capture_snapshot(pipeline, start_pipeline=True, batches=1, wait=False)

        time.sleep(1)
        mqtt_broker.publish_message(topic=data_topic, payload=payload)
        snapshot = running_snapshot.wait_for_finished().snapshot
        sdc_executor.stop_pipeline(pipeline)
        # write your assertion code here
    finally:
        mqtt_broker.destroy()"""

        if self.file_name == 'test_influxdb_destination.py':
            stage_attributes = ', **stage_attributes' if 'stag_attributes' in self.line else ''

            line = f"""{self.line[0:len(self.line)-3]}, influxdb):
    client = influxdb.client
    measurement = get_random_string(string.ascii_letters, 10)
    raw_dict = [{{'measurement': measurement, 'record': {{'time': 1439897881000, 'butterflies': 12, 'honeybees': 23,
                                                        'location': '1', 'scientist': 'langstroth'}}}}]
    create_db = not any(database['name'] == influxdb.database for database in client.get_list_database())

    try:
        # build pipeline and get the same
        pipeline, destination = get_pipeline_and_destination_stage(raw_dict, sdc_builder, influxdb, create_db{stage_attributes})
        #want to set attribute after configure for env ? set here.
        
    finally:
        if sdc_executor.get_pipeline_status(pipeline).response.json().get('status') == "RUNNING":
            sdc_executor.stop_pipeline(pipeline)
        logger.info('Dropping InfluxDB measurement %s in the database %s ...', measurement, influxdb.database)
        influxdb.drop_measurement(measurement)
        logger.info('Dropping InfluxDB database %s ...', influxdb.database)
        client.drop_database(influxdb.database)"""

        return line







