import json
import os


class GoldConfig:
    def __init__(self, config_repo_path, source_system, env, territory):
        self.config_repo_path = config_repo_path
        self.source_system = source_system
        self.env = env
        self.territory = territory

    def remove_tasks_from_workflow(self, task_names):
        # Construct the path to the combined-workflows.json file
        workflow_file_path = os.path.join(self.config_repo_path, 'configs', self.source_system,
                                    self.territory, self.env, 'vitruvian-workflows',
                                    f"{self.source_system}-{self.territory}-{self.env}-combined-workflows.json")

        if not os.path.isfile(workflow_file_path):
            print(f"No such file: {workflow_file_path}")
            return

        with open(workflow_file_path, 'r') as f:
            workflows = json.load(f)

        # Iterate through each workflow and task, removing tasks that match the provided task_names
        for workflow in workflows:
            if "tasks" in workflow:
                removed_tasks = [task['key'] for task in workflow['tasks'] if task['key'] in task_names]
                print(f"Found and removing tasks: {removed_tasks}")
                workflow['tasks'] = [task for task in workflow['tasks'] if task['key'] not in task_names]

        # Save the modified JSON back to the file
        with open(workflow_file_path, 'w') as f:
            json.dump(workflows, f, indent=4)
            f.write('\n') 
