import logging as log
from argparse import ArgumentParser
from datetime import datetime, date
from pydantic import BaseModel

# Default files
data_file = "config/data.yml"
params_file = "config/params.yml"
output_file = "timeline.svg"


class Parser:
    def __init__(self):
        self.__parser = ArgumentParser(
            "description=Generate a timeline for your books."
        )
        self.__parser.add_argument(
            "-v",
            "--verbosity",
            action="count",
            default=0,
            help="increase output verbosity (e.g., -vv is more than -v)",
        )
        self.__parser.add_argument(
            "-d", "--data_file", required=False, help="Path to the data file (YAML)"
        )
        self.__parser.add_argument(
            "-p", "--params_file", required=False, help="Path to the params file (YAML)"
        )
        self.__parser.add_argument(
            "-o", "--output_file", required=False, help="Path for the output file (SVG)"
        )
        self.__parser.add_argument(
            "--from",
            required=False,
            dest="from_",
            help="Overrides the *from* value on the data file",
        )
        self.__parser.add_argument(
            "--to", required=False, help="Overrides the *to* value on the data file"
        )

    def get_args(self):
        return self.__parser.parse_args()


class Args:
    def __init__(self):
        self.__args = Parser().get_args()

    def get_verbosity(self) -> int:
        return min(self.__args.verbosity, 2)

    def get_data_file(self) -> str:
        if self.__args.data_file is not None:
            return self.__args.data_file
        return data_file

    def get_params_file(self) -> str:
        if self.__args.params_file is not None:
            return self.__args.params_file
        return params_file

    def get_output_file(self) -> str:
        if self.__args.output_file is not None:
            return self.__args.output_file
        return output_file

    def get_from(self) -> date | None:
        if self.__args.from_ is None:
            return None
        try:
            return datetime.strptime(self.__args.from_, "%Y-%m-%d").date()
        except ValueError:
            log.error(
                "Cannot parse *from* argument. Ensure it follows the format YYYY-MM-DD."
            )
            exit(1)

    def get_to(self) -> date | None:
        if self.__args.to is None:
            return None
        try:
            return datetime.strptime(self.__args.to, "%Y-%m-%d").date()
        except ValueError:
            log.error(
                "Cannot parse *to* argument. Ensure it follows the format YYYY-MM-DD."
            )
            exit(1)


class DataArgs(BaseModel):
    from_: date | None = None
    to: date | None = None
