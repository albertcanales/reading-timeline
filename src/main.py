try:
    import logging as log
    from args import Args
    from logs import set_log_verbosity
    from yml import read_yml
    from data import Data
    from params import Params
    from processor import Processor
    from drawer import draw
except ModuleNotFoundError:
    log.error(
        "Modules not found. Ensure you have installed dependencies with *make install*"
    )
    exit(1)


def main():
    args = Args()
    set_log_verbosity(args.get_verbosity())

    # Read data file
    log.info("Reading input data...")
    data_dict = read_yml(args.get_data_file())
    data = Data(data_dict)
    log.info(data)

    # Read params file
    log.info("Reading parameters...")
    params_dict = read_yml(args.get_params_file())
    params = Params(params_dict)

    # Process data using the parameters
    log.info("Applying parameters to data...")
    process = Processor(data, params)

    # Draw the image from processed data and parameters
    log.info("Drawing SVG...")
    draw(args.get_output_file(), params, process)
    log.info("Drawing done")


if __name__ == "__main__":
    main()