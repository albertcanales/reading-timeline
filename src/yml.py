import yaml


def read_yml(path):
    try:
        file = open(path, "r")
        d = yaml.load(file, Loader=yaml.FullLoader)
        return d
    except IOError:
        log.error("Could not load %s." % path)
        exit(1)
    except yaml.YAMLError:
        log.error("Invalid YAML in %s." % path)
        exit(1)
