import itertools
from config_processors.cmt_config import CMTConfig
from config_processors.gold_config import GoldConfig
from config_processors.silver_config import SilverConfig

ENVS = ["int", "prod"]
TERRITORIES = ["na-us-nj", "na-us-pa", "na-ca-on", "eu"]


def run_all_silver(config_repo_path, source_system, table_names):
    print("\n🥈 Updating Silver pipelines\n")
    for env, territory in itertools.product(ENVS, TERRITORIES):
        print("\nFor: ", env, territory, "\n-------------")
        config = SilverConfig(config_repo_path, source_system, env, territory)
        config.remove_table_entries(table_names)


def build_all_silver_metadata(config_repo_path, source_system):
    print("\n🥈 Updating Silver pipelines\n")
    for env, territory in itertools.product(ENVS, TERRITORIES):
        print("\nFor: ", env, territory, "\n-------------")
        config = SilverConfig(config_repo_path, source_system, env, territory)
        config.build_metadata()


def run_all_gold(config_repo_path, source_system, task_names):
    print("\n🥇 Updating Gold pipelines\n")
    for env, territory in itertools.product(ENVS, TERRITORIES):
        print("\nFor: ", env, territory, "\n-------------")
        config = GoldConfig(config_repo_path, source_system, env, territory)
        config.remove_tasks_from_workflow(task_names)


def run_all_cmt(config_repo_path, source_system, cmt_version):
    print("\n🛠 Updating CMT pipelines\n")
    for territory in TERRITORIES:
        print("\nFor: ", territory, "\n-------------")
        config = CMTConfig(config_repo_path, source_system, territory)
        config.update_artifact_version(cmt_version)


# run_all_silver("../vitruvian-deployment-configurations/", "excite", ["comp_type_v1"])
# run_all_gold("../vitruvian-deployment-configurations/", "excite", ["fct_compensation_event","fct_payment_event"])
# run_all_cmt("../vitruvian-deployment-configurations/", "excite", "1.0.575")
# build_all_silver_metadata("../vitruvian-deployment-configurations/", "excite")

silverConfig = SilverConfig(
    "../vitruvian-deployment-configurations/", "excite", "prod", "eu"
)
# silverConfig.remove_table_entries(["compensation_v1", "comp_type_v1"])
# silverConfig.build_metadata()
silverConfig.unpause_tables(["comp_type_v1"])
# goldconfig = GoldConfig("../vitruvian-deployment-configurations/","excite","int","na-us-nj")
# goldconfig.remove_tasks_from_workflow(["fct_compensation_event","fct_payment_event"])
# cmt_config = CMTConfig("../vitruvian-deployment-configurations/", "excite", "na-us-nj")
# cmt_config.update_artifact_version("1.0.556")
