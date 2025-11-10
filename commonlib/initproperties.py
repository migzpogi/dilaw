import configparser


class InitProperties:
    """
    Parses an .ini file for application configuration

    Given a bar.ini file:
        [section_a]
        host = localhost
        port = 8080

    Usage:
        foo = InitProperties('bar.ini')
        print(foo.config.get('section_a', 'host'))

    * Always return values as strings
    """
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.__load_config()

    def __load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)

        return config

    def webapp(self):
        """Expected sections and options used for WebApp"""
        try:
            webapp_config = {
                'host': self.config.get('webapp', 'host'),
                'port': self.config.get('webapp', 'port')
            }

            return webapp_config
        except configparser.NoSectionError as e:
            print('ERROR: Expected section "webapp" is not found in the .ini file')
        except configparser.NoOptionError as e:
            print('ERROR: Expected option "host" or "port" is not found in the .ini file')


