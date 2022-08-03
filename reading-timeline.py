import yaml
import data as dat
import config as con
import processor as proc
import drawer as drw

def read_yaml(path):
    try:
        file = open(path, 'r')
        d = yaml.load(file, Loader=yaml.FullLoader)
        return d
    except IOError:
        print("Could not load %s." % path)
        exit(1)
    except yaml.YAMLError:
        print("Invalid YAML in %s." % path)
        exit(1)

def main():
    # Read data file
    data_dict = read_yaml('data.yml')
    data = dat.Data(data_dict)

    # Read the configuration
    config_dict = read_yaml('config.yml')
    config = con.Config(config_dict)

    # Process data using the configuration
    process = proc.Processor(data, config)

    # Draw the image from processed data and configuration
    drw.draw('render.svg', config, process)

if __name__ == "__main__":
    main()
