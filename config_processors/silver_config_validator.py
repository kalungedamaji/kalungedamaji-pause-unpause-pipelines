import json


class SilverConfigValidator:
    @staticmethod
    def is_valid_json_string(json_str):
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return False

    @staticmethod
    def validate_config_file(file_path):
        with open(file_path, "r") as f:
            config_data = json.load(f)
        invalid_job_names = []
        for job_name, values in config_data.items():
            if len(values) > 1 and not SilverConfigValidator.is_valid_json_string(
                values[1]
            ):
                invalid_job_names.append(job_name)

        if invalid_job_names:
            print(f"Invalid JSON string for job(s): {invalid_job_names}")
            return False
        return True
