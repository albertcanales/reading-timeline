import yaml
import drawSvg as draw
import config as conf

def read_config(path):
    try:
        file = open(path, 'r')
        config_dict = yaml.load(file, Loader=yaml.FullLoader)
        return config_dict
    except IOError:
        print("Could not load the configuration file.")
        exit(1)
    except yaml.YAMLError:
        print("Invalid YAML in configuration file.")
        exit(1)

def main():
    # Read configuration file
    config_dict = read_config('config.yml')
    config = conf.Config(config_dict)

    print(config)

    # Calculate positions and sizes
    pass

    # Draw the SVG
    pass

if __name__ == "__main__":
    main()
