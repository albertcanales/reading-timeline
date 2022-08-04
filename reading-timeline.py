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
    print("Reading input data...")
    data_dict = read_yaml('data.yml')
    data = dat.Data(data_dict)
    print(data, "\n")

    # Read the configuration
    print("Reading configuration...")
    config_dict = read_yaml('config.yml')
    config = con.Config(config_dict)
    print()

    # Process data using the configuration
    print("Applying configuration to data...")
    process = proc.Processor(data, config)
    print()

    # Draw the image from processed data and configuration
    print("Drawing SVG...")
    drw.draw('render.svg', config, process)
    print("Drawing done")

if __name__ == "__main__":
    main()
