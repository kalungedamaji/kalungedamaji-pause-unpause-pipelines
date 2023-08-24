import json
import os
import re
from config_processors.silver_config_validator import SilverConfigValidator


class SilverConfig:
    def __init__(self, config_repo_path, source_system, env, territory):
        self.config_repo_path = config_repo_path
        self.source_system = source_system
        self.env = env
        self.territory = territory

    def remove_table_entries(self, table_names):
        print("Removing tables: ", table_names)

        config_dir = os.path.join(
            self.config_repo_path,
            "configs",
            self.source_system,
            self.territory,
            self.env,
        )

        app_vars_file = os.path.join(config_dir, "app_vars.json")

        if not os.path.isfile(app_vars_file):
            print(f"No such file: {app_vars_file}")
            return

        with open(app_vars_file, "r") as f:
            app_vars = json.load(f)

        table_names = set(table_names)  # convert list to set for faster operations

        # Initialize a dictionary to store removed tables
        removed_matches = {}

        for job, values in app_vars.items():
            if len(values) > 1 and isinstance(values[1], str):
                for table_name in table_names:
                    table_entry_str = (
                        f'{{ "database_name": "[^"]*", "table_name":"{table_name}" }}'
                        + ","
                    )
                    matches = re.findall(table_entry_str, values[1])
                    if matches:
                        print("\nEnrichment job::", job)
                        if job not in removed_matches:
                            removed_matches[job] = []
                        for match in matches:
                            print(f"Removing Matching record: {match}")
                        values[1] = re.sub(table_entry_str, "", values[1])

        with open(app_vars_file, "w") as f:
            json.dump(app_vars, f, indent=4)
            f.write("\n")

        self.validate_config_file(app_vars_file)

    def unpause_tables(self, table_names):
        print("Unpausing tables: ", table_names)

        metadata_file_path = os.path.join(
            "metadata", f"{self.territory}-{self.env}-app-vars.json"
        )
        app_vars_file_path = os.path.join(
            self.config_repo_path,
            "configs",
            "excite",
            self.territory,
            self.env,
            "app_vars.json",
        )
        with open(metadata_file_path, "r") as f:
            metadata = json.load(f)

        with open(app_vars_file_path, "r") as f:
            app_vars = json.load(f)

        for table_name in table_names:
            if table_name in metadata:
                job_name = metadata[table_name]["job_name"]
                value_string = metadata[table_name]["value"]

                if job_name in app_vars:
                    if table_name in app_vars[job_name][1]:
                        raise ValueError(
                            f"Error Processing::Table {table_name} already exists in {job_name}"
                        )
                    app_vars[job_name][1] = re.sub(
                        r"\]$", f", {value_string}]", app_vars[job_name][1]
                    )
                    print("\nEnrichment job::", job_name)
                    print(f"Adding table {value_string}")
                else:
                    raise ValueError(f"Job {job_name} not found in app_vars.json")
            else:
                raise ValueError(f"Table {table_name} not found in metadata")

        with open(app_vars_file_path, "w") as f:
            json.dump(app_vars, f, indent=4)
            f.write("\n")

        self.validate_config_file(app_vars_file_path)

    def validate_config_file(self, app_vars_file_path):
        validator = SilverConfigValidator()
        if not validator.validate_config_file(app_vars_file_path):
            raise ValueError(f"Invalid Config file: {app_vars_file_path}")

    def build_metadata(self):
        config_dir = os.path.join(
            self.config_repo_path,
            "configs",
            self.source_system,
            self.territory,
            self.env,
        )
        source_file_path = os.path.join(config_dir, "app_vars.json")

        if not os.path.isfile(source_file_path):
            raise FileNotFoundError(f"No such file: {source_file_path}")

        with open(source_file_path, "r") as source_file:
            data = json.load(source_file)

        metadata = {}

        # Traverse the jobs in the data
        for job_name, values in data.items():
            if len(values) > 1 and isinstance(values[1], str):
                try:
                    tables = json.loads(values[1])  # parse json string that has tables
                except json.JSONDecodeError:
                    raise ValueError(
                        f"Invalid JSON string in the value array for {job_name}"
                    )

                for table in tables:
                    table_name = table["table_name"]
                    if table_name in metadata:  # Check if table_name already exists
                        raise ValueError(f"Duplicate table name detected: {table_name}")

                    metadata[table_name] = {
                        "value": json.dumps(table, separators=(",", ":")),
                        "job_name": job_name,
                    }

        # save the metadata file
        output_file_path = os.path.join(
            "metadata", f"{self.territory}-{self.env}-app-vars.json"
        )
        with open(output_file_path, "w") as output_file:
            json.dump(metadata, output_file, indent=4)

        print(f"Metadata saved to: {output_file_path}")
