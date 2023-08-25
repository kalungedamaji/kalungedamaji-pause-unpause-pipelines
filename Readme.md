## Utility to pause unpause pipelines

### Project structure

```
project_root/
|-- config_processors/
| |-- cmt_config.py
| |-- gold_config.py
| |-- silver_config.py
|
|--run.py
|--main.py
```

### List of todos/enhacements
[Todos](todo.md)

### Metadata files

- to aid in adding/removing tables the app_vars json files are parsed
- for each table entry metadata is maintained that gives table name and value to substitute
- example metadata entry for member_kyc table on eu

```json
 "member_kyc_event_v1": {
        "value": "{\"database_name\":\"vitruvian_excite_eu_silver_verification\",\"table_name\":\"member_kyc_event_v1\"}",
        "job_name": "excite_eu_int_data-enrichment-app_parameters-2"
    },
```

### Command line

- still to improve, run via python for now

```console
python3 main.py --config_repo_path ../vitruvian-deployment-configurations/ --source_system excite --pipeline silver --env int --territory  na-us-nj --table_names compensation_v1,member_kyc_event_v1

```

- CMT update artifact version command

```console
python3 main.py --config_repo_path ../vitruvian-deployment-configurations/ --source_system excite --pipeline cmt --env int --territory na-us-nj --cmt_version 1.0.533

```

### Run via python

- open run.py and supply params directly using python code
- just run from vscode/ide or from terminal use command below

```console
/usr/bin/python3 /Users/atul.verma/projects/ballys/pause-unpause-pipelines/run.py
```

- example below shows functions to call to pause or unpause tables

```python
silverConfig = SilverConfig(
    "../vitruvian-deployment-configurations/", "excite", "prod", "eu"
)
silverConfig.remove_table_entries(["compensation_v1", "comp_type_v1"])
silverConfig.unpause_tables(["comp_type_v1"])
```
