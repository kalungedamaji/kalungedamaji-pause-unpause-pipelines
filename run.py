import itertools
from config_processors.cmt_config import CMTConfig
from config_processors.gold_config import GoldConfig
from config_processors.silver_config import SilverConfig
from git_operations.git_operation import commit_and_push_code
from git_operations.git_operation  import checkout_configuration_repo
ENVS = ["int", "prod"]
TERRITORIES = ["na-us-nj", "na-us-pa", "na-ca-on", "eu"]


def run_all_silver(config_repo_path, jira_ticket_no, source_system, table_names):
    print("\n🥈 Updating Silver pipelines\n")
    for env, territory in itertools.product(ENVS, TERRITORIES):
        print("\nFor: ", env, territory, "\n-------------")
        config = SilverConfig(config_repo_path, source_system, env, territory)
        config.remove_table_entries(table_names)

    commit_and_push_code(config_repo_path, jira_ticket_no + "_pause_enrichment_app_for_all_env",
                         jira_ticket_no + " | Paused table " + ', '.join(map(str, table_names)))


def build_all_silver_metadata(config_repo_path, source_system):
    print("\n🥈 Updating Silver pipelines\n")
    for env, territory in itertools.product(ENVS, TERRITORIES):
        print("\nFor: ", env, territory, "\n-------------")
        config = SilverConfig(config_repo_path, source_system, env, territory)
        config.build_metadata()


def run_all_gold(config_repo_path, jira_ticket_no, source_system, task_names):
    print("\n🥇 Updating Gold pipelines\n")
    for env, territory in itertools.product(ENVS, TERRITORIES):
        print("\nFor: ", env, territory, "\n-------------")
        config = GoldConfig(config_repo_path, source_system, env, territory)
        config.remove_tasks_from_workflow(task_names)
    commit_and_push_code(config_repo_path, jira_ticket_no + "_pause_gold_pipeline_for_all_env",
                         jira_ticket_no + " | Paused gold task " + ', '.join(map(str, task_names)))


def run_all_cmt(config_repo_path, source_system, cmt_version):
    print("\n🛠 Updating CMT pipelines\n")
    for territory in TERRITORIES:
        print("\nFor: ", territory, "\n-------------")
        config = CMTConfig(config_repo_path, source_system, territory)
        config.update_artifact_version(cmt_version)
    commit_and_push_code(config_repo_path, "update_cmt_version_for_all_env",
                         "Updated the CMT version to " + cmt_version)


def run_all_silver_unpause(config_repo_path, jira_ticket_no, source_system, table_names):
    print("\n🥈 Updating Silver pipelines\n")
    for env, territory in itertools.product(ENVS, TERRITORIES):
        print("\nFor: ", env, territory, "\n-------------")
        config = SilverConfig(config_repo_path, source_system, env, territory)
        config.unpause_tables(table_names)
    commit_and_push_code(config_repo_path, jira_ticket_no + "_un_pause_enrichment_app_for_all_env",
                         jira_ticket_no + " | un-paused table " + ', '.join(map(str, table_names)))


def pause_enrichment_app_for_one_env(config_repo_path, jira_ticket_no, data_source, env, region, table_names):
    silverConfig = SilverConfig(config_repo_path, data_source, env, region)
    silverConfig.remove_table_entries(table_names)
    commit_and_push_code(config_repo_path, jira_ticket_no + "_un_pause_enrichment_app_for_" + region,
                         jira_ticket_no + " | un-paused table " + ', '.join(map(str, table_names)))

# Run for all environments and territories
run_all_silver("../pythonProject/vitruvian-deployment-configurations/", "DSE-10171", "excite",
               ["command_audit_v1", "high_roller_audit_v1", "campaign_audit_v1"])
# run_all_silver_unpause(
#    "../vitruvian-deployment-configurations/", "excite", ["comp_type_v1"]
# )

# run_all_gold("../pythonProject/vitruvian-deployment-configurations/", "excite", ["dim_account_managed_status"])
# run_all_cmt("../vitruvian-deployment-configurations/", "excite", "1.0.575")

# Build or refresh metadata for all silver tables
# build_all_silver_metadata("../vitruvian-deployment-configurations/", "excite")

#  Run for specific environment and territory

# silverConfig = SilverConfig(
#    "../vitruvian-deployment-configurations/", "excite", "prod", "na-us-nj"
# )
# silverConfig.remove_table_entries(["comp_type_v1"])
# silverConfig.build_metadata()
# silverConfig.unpause_tables(["comp_type_v1"])

# goldconfig = GoldConfig("../vitruvian-deployment-configurations/","excite","int","na-us-nj")
# goldconfig.remove_tasks_from_workflow(["fct_compensation_event","fct_payment_event"])

# cmt_config = CMTConfig("../vitruvian-deployment-configurations/", "excite", "na-us-nj")
# cmt_config.update_artifact_version("1.0.556")
