def load_config_to_globals(filepath):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(filepath)
    for section in config.sections():
        for key, value in config.items(section):
            var_name = f"{key}"              #f"{section}_{key}"
            try:
                globals()[var_name] = int(value)
            except:
                try :
                    globals()[var_name] = eval(value)
                except :
                    globals()[var_name] = value