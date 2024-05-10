# util/db_property_util.py
import configparser

def get_connection_string(property_file):
    config = configparser.ConfigParser()
    config.read(property_file)
    connection_string = config.get('database', 'connection_string')
    return connection_string

