class PipelineBuilderCode:
    def __init__(self, file_name, line):
        self.line = line
        self.file_name = file_name

    def build_pipeline(self):
        pipeline_builder = 'pipeline_builder = sdc_builder.get_pipeline_builder()'
        trash = "trash = pipeline_builder.add_stage('Trash')"
        if self.file_name == 'test_mqtt_subscriber_origin.py':
            if 'stage_attributes' in self.line:
                stage_attributes = ', **stage_attributes'
                source_set_attributes = 'mqtt_source.set_attributes(**stage_attributes)'
            line = f"""
# util function
def get_mqtt_trash_pipeline_and_mqtt_stage(sdc_builder, mqtt_broker{stage_attributes}):
    {pipeline_builder}
    mqtt_source = pipeline_builder.add_stage('MQTT Subscriber')
    {source_set_attributes}
    {trash}
    mqtt_source >> trash
    pipeline = pipeline_builder.build().configure_for_environment(mqtt_broker)
    return pipeline, mqtt_source"""
        elif self.file_name == 'test_influxdb_destination.py':
            stage_attributes = ',**stage_attributesn' if 'stage_attributes' in self.line else ''

            line = f"""
# util function            
def get_pipeline_and_destination_stage(raw_dict, sdc_builder, influxdb, create_db{stage_attributes}):
    # build pipeline ,returns pipeline and influxdb stage as destination
    raw_data = json.dumps(raw_dict)
    {pipeline_builder}
    dev_raw_data_source = builder.add_stage('Dev Raw Data Source')
    dev_raw_data_source.set_attributes(data_format='JSON', json_content='ARRAY_OBJECTS', raw_data=raw_data)
    influxdb_destination = builder.add_stage('InfluxDB', type='destination')
    influxdb_destination.set_attributes(auto_create_database=create_db,
                                        record_mapping='CUSTOM',
                                        measurement_field='/measurement',
                                        time_field='/record/time',
                                        time_unit='MILLISECONDS',
                                        tag_fields=["/record/location", "/record/scientist"],
                                        value_fields=["/record/butterflies", "/record/honeybees"]{stage_attributes})
    dev_raw_data_source >> influxdb_destination
    pipeline = builder.build().configure_for_environment(influxdb)
    return pipeline, influxdb_destination"""
        elif self.file_name == 'test_mqtt_publisher_destination.py':
            stage_attributes = ', **stage_attributes' if 'stage_attributes' in self.line else ''
            line = f"""
# util function 
def get_pipeline_and_stages(sdc_builder, data_topic, mqtt_broker{stage_attributes}):
    {pipeline_builder}
    raw_str = 'dummy_value'
    dev_raw_data_source = pipeline_builder.add_stage('Dev Raw Data Source')
    dev_raw_data_source.set_attributes(data_format='TEXT', raw_data=raw_str)
    mqtt_target = pipeline_builder.add_stage('MQTT Publisher')
    mqtt_target.set_attributes(topic=data_topic, data_format='TEXT'{stage_attributes})
    dev_raw_data_source >> mqtt_target
    pipeline = pipeline_builder.build().configure_for_environment(mqtt_broker)
    return pipeline, mqtt_target, dev_raw_data_source"""

        elif self.file_name == 'test_mongodb_origin.py':
            stage_attributes = ', **stage_attributes' if 'stage_attributes' in self.line else ''
            line = f"""
# util function
def get_mongodb_to_trash_pipeline_and_stage(sdc_builder, mongodb{stage_attributes}):
    {pipeline_builder}
    pipeline_builder.add_error_stage('Discard')
    mongodb_origin = pipeline_builder.add_stage('MongoDB', type='origin')
    mongodb_origin.set_attributes(capped_collection=False,
                                  database=get_random_string(),
                                  collection=get_random_string(){stage_attributes})
    {trash}
    mongodb_origin >> trash
    pipeline = pipeline_builder.build().configure_for_environment(mongodb)
    return pipeline, mongodb_origin"""
        elif self.file_name == 'test_redis_consumer_origin.py':
            stage_attributes = ', **stage_attributes' if 'stage_attributes' in self.line else ''
            line = f"""
# util function 
def get_redis_origin_to_trash_pipeline(sdc_builder, redis{stage_attributes}
    {pipeline_builder}
    redis_consumer = builder.add_stage('Redis Consumer', type='origin')
    redis_consumer.set_attributes(data_format='JSON', max_batch_size_in_records=10,
                                  pattern=[f'*{pattern_1}*'])
    


"""
        return line
