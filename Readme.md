### Utility to pause unpause pipelines

#### project structure

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

#### command line

- still to improve, run via python for now

```
python3 main.py --config_repo_path ../vitruvian-deployment-configurations/ --source_system excite --pipeline silver --env int --territory  na-us-nj --table_names compensation_v1,member_kyc_event_v1

```

- CMT update artifact version command

```
python3 main.py --config_repo_path ../vitruvian-deployment-configurations/ --source_system excite --pipeline cmt --env int --territory na-us-nj --cmt_version 1.0.533

```

#### run via python

- open run.py and supply params directly using python code
- just run from vscode/ide or from terminal use command below

```
/usr/bin/python3 /Users/atul.verma/projects/ballys/pause-unpause-pipelines/run.py
```
