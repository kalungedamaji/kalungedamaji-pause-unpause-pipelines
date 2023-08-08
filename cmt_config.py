import os
import json

class CMTConfig:
    def __init__(self, config_repo_path, source_system, territory):
        self.config_repo_path = config_repo_path
        self.source_system = source_system
        self.territory = territory

    def update_artifact_version(self, cmt_version):
        # Construct the path to the json file
        file_path = os.path.join(self.config_repo_path, "change-management", self.source_system, self.territory, f"{self.source_system}_{self.territory}_database.json")

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        # Update the artifact_version
        for definition in data["system_definition"]:
            if definition["system"] == self.source_system:
                old_version = definition["schema_definition"]["artifact_version"]
                definition["schema_definition"]["artifact_version"] = cmt_version
                print(f"Updating from {old_version} to {cmt_version}")

        # Write back the updated data to the json file
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
            json_file.write('\n') 
