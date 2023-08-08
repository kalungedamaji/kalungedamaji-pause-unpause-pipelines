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
        config_dir = os.path.join(self.config_repo_path, 'configs',
                                self.source_system, self.territory, self.env)

        app_vars_file = os.path.join(config_dir, 'app_vars.json')

        if not os.path.isfile(app_vars_file):
            print(f"No such file: {app_vars_file}")
            return

        with open(app_vars_file, 'r') as f:
            app_vars = json.load(f)

        table_names = set(table_names) # convert list to set for faster operations

        for job, values in app_vars.items():
            if len(values) > 1 and isinstance(values[1], str):  # Check if there are at least 2 elements and values[1] is a string
                for table_name in table_names:
                    table_entry_str = f'{{ "database_name": "[^"]*", "table_name":"{table_name}" }}'+ ","
                    matches = re.findall(table_entry_str, values[1])
                    if len(matches) > 0:
                        print("Enrichment job::", job)
                    for match in matches:
                        print(f"Removing Matching record: {match}")

                    values[1] = re.sub(table_entry_str, '', values[1])

                # print(values[1])
                # tables = json.loads(values[1])
                # removed_tables = [table for table in tables if table['table_name'] in table_names]
                # print(f"For job {job}, removed tables: {removed_tables}")
            # values[1] = json.dumps(updated_tables, separators=(', ', ':'))

        with open(app_vars_file, 'w') as f:
            json.dump(app_vars, f, indent=4)
            f.write('\n') 
