import logging as log
import argparse

# Set log and args configuration
log.basicConfig(format="%(levelname)s: %(message)s\n")
parser = argparse.ArgumentParser("description=Generate a timeline for your books.")
parser.add_argument('-v', '--verbosity', action="count", default=0,
                    help="increase output verbosity (e.g., -vv is more than -v)")
parser.add_argument('-d', '--data_file', required=False,
                    help='Path to the data file (YAML)')
parser.add_argument('-c', '--config_file', required=False,
                    help='Path to the config file (YAML)')
parser.add_argument('-o', '--output_file', required=False,
                    help='Path for the output file (SVG)')
args = parser.parse_args()

try:
    import yaml
    import data as dat
    import config as con
    import processor as proc
    import drawer as drw
except ModuleNotFoundError:
    log.error("Modules not found. Ensure venv is used and requirements are installed.")
    exit(1)

data_file = 'data.yml'
config_file = 'config.yml'
output_file = 'timeline.svg'

# Returns the dictionary from the given yaml file path
def read_yaml(path):
    try:
        file = open(path, 'r')
        d = yaml.load(file, Loader=yaml.FullLoader)
        return d
    except IOError:
        log.error("Could not load %s." % path)
        exit(1)
    except yaml.YAMLError:
        log.error("Invalid YAML in %s." % path)
        exit(1)

def main():
    # Get arg verbosity
    log_levels = [log.ERROR, log.WARNING, log.INFO]
    args.verbosity = min(args.verbosity, 2)
    log.basicConfig(level=log_levels[args.verbosity])

    # Get arg files
    global data_file, config_file, output_file
    if args.data_file is not None:
        data_file = args.data_file
    if args.config_file is not None:
        config_file = args.config_file
    if args.output_file is not None:
        output_file = args.output_file

    # Read data file
    log.info("Reading input data...")
    data_dict = read_yaml(data_file)
    data = dat.Data(data_dict)
    log.info(data)

    # Read the configuration
    log.info("Reading configuration...")
    config_dict = read_yaml(config_file)
    config = con.Config(config_dict)

    # Process data using the configuration
    log.info("Applying configuration to data...")
    process = proc.Processor(data, config)

    # Draw the image from processed data and configuration
    log.info("Drawing SVG...")
    drw.draw(output_file, config, process)
    log.info("Drawing done")

if __name__ == "__main__":
    main()
