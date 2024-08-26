import logging as log
import argparse

# Default files
data_file = "config/data.yml"
params_file = "config/params.yml"
output_file = "timeline.svg"


class Args:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            "description=Generate a timeline for your books."
        )
        self.parser.add_argument(
            "-v",
            "--verbosity",
            action="count",
            default=0,
            help="increase output verbosity (e.g., -vv is more than -v)",
        )
        self.parser.add_argument(
            "-d", "--data_file", required=False, help="Path to the data file (YAML)"
        )
        self.parser.add_argument(
            "-p", "--params_file", required=False, help="Path to the params file (YAML)"
        )
        self.parser.add_argument(
            "-o", "--output_file", required=False, help="Path for the output file (SVG)"
        )
        self.args = self.parser.parse_args()

    def get_verbosity(self) -> int:
        return min(self.args.verbosity, 2)

    def get_data_file(self) -> str:
        if self.args.data_file is not None:
            return self.args.data_file
        return data_file

    def get_params_file(self) -> str:
        if self.args.params_file is not None:
            return self.args.params_file
        return params_file

    def get_output_file(self) -> str:
        if self.args.output_file is not None:
            return self.args.output_file
        return output_file
