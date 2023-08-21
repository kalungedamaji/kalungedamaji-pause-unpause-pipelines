import json
import os
import re


class SilverConfig:
    def __init__(self, config_repo_path, source_system, env, territory):
        self.config_repo_path = config_repo_path
        self.source_system = source_system
        self.env = env
        self.territory = territory

    def remove_table_entries(self, table_names):
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
                    table_entry_str = f'{{ "database_name": "[^"]*", "table_name":"{table_name}" }}' + ","
                    matches = re.findall(table_entry_str, values[1])
                    if matches:
                        print("Enrichment job::", job)
                        if job not in removed_matches:
                            removed_matches[job] = []
                        for match in matches:
                            print(f"Removing Matching record: {match}")
                            removed_matches.setdefault(self.env, {}).setdefault(self.territory, {}).setdefault(
                                job, []
                            ).setdefault(table_name, {}).append(match)
                        print(f"removed_matches: {removed_matches}")
                        values[1] = re.sub(table_entry_str, "", values[1])

        with open(app_vars_file, "w") as f:
            json.dump(app_vars, f, indent=4)
            f.write("\n")

        # Save the removed tables to the file
        with open("paused/removed-silver-tables.json", "w") as f:
            json.dump(removed_matches, f, indent=4)

    def unpause_tables(self, table_names):
        paused_file_path = "paused/removed-silver-tables.json"

        # Step 1: Load the paused entries
        with open(paused_file_path, "r") as f:
            paused_entries = json.load(f)

        config_dir = os.path.join(
            self.config_repo_path,
            "configs",
            self.source_system,
            self.territory,
            self.env,
        )
        app_vars_file = os.path.join(config_dir, "app_vars.json")

        # Load app_vars.json
        with open(app_vars_file, "r") as f:
            app_vars = json.load(f)

        for table_name in table_names:
            # Get the paused entries for table_name
            for job_name, removed_entries in paused_entries.items():
                # Filter to find a matching entry
                matching_entries = [entry for entry in removed_entries if f'"table_name":"{table_name}"' in entry]

                # If we found a match, update app_vars
                if matching_entries:
                    print("Enrichment job::", job_name)
                    print(f"matching_entries: {matching_entries}")

                    app_vars[job_name][1] += "".join(matching_entries)
                    paused_entries[job_name] = [
                        entry for entry in paused_entries[job_name] if entry not in matching_entries
                    ]

        with open(app_vars_file, "w") as f:
            json.dump(app_vars, f, indent=4)
            f.write("\n")

        with open(paused_file_path, "w") as f:
            json.dump(paused_entries, f, indent=4)
