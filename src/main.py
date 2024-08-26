import logging as log
import argparse

# Set log and args configuration
log.basicConfig(format="%(levelname)s: %(message)s\n")
parser = argparse.ArgumentParser("description=Generate a timeline for your books.")
parser.add_argument('-v', '--verbosity', action="count", default=0,
                    help="increase output verbosity (e.g., -vv is more than -v)")
parser.add_argument('-d', '--data_file', required=False,
                    help='Path to the data file (YAML)')
parser.add_argument('-p', '--params_file', required=False,
                    help='Path to the params file (YAML)')
parser.add_argument('-o', '--output_file', required=False,
                    help='Path for the output file (SVG)')
args = parser.parse_args()

try:
    import yaml
    import data as dat
    import params as par
    import processor as proc
    import drawer as drw
except ModuleNotFoundError:
    log.error("Modules not found. Ensure venv is used and requirements are installed.")
    exit(1)

data_file = 'config/data.yml'
params_file = 'config/params.yml'
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
    global data_file, params_file, output_file
    if args.data_file is not None:
        data_file = args.data_file
    if args.params_file is not None:
        params_file = args.params_file
    if args.output_file is not None:
        output_file = args.output_file

    # Read data file
    log.info("Reading input data...")
    data_dict = read_yaml(data_file)
    data = dat.Data(data_dict)
    log.info(data)

    # Read params file
    log.info("Reading parameters...")
    params_dict = read_yaml(params_file)
    params = par.Params(params_dict)

    # Process data using the parameters
    log.info("Applying parameters to data...")
    process = proc.Processor(data, params)

    # Draw the image from processed data and parameters
    log.info("Drawing SVG...")
    drw.draw(output_file, params, process)
    log.info("Drawing done")

if __name__ == "__main__":
    main()
