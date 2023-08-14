import argparse
import itertools

from silver_config import SilverConfig
from gold_config import GoldConfig
from cmt_config import CMTConfig


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pause_unpause_bool", required=False)
    parser.add_argument("--config_repo_path", required=True)
    parser.add_argument("--source_system", required=True)
    parser.add_argument(
        "--pipeline",
        required=True,
        help="Name of the pipeline. Accepted values: gold, silver, cmt.",
    )
    parser.add_argument(
        "--cmt_version",
        required=False,
        help="CMT artifact version. This is required if the pipeline is cmt.",
    )
    parser.add_argument("--env", required=True)
    parser.add_argument("--territory", required=True)
    parser.add_argument("--table_names", nargs="*", required=False)
    parser.add_argument("--task_names", nargs="*", required=False)
    return parser.parse_args()


def main():
    args = get_args()

    print("User Input Arguments:")
    print("-" * 50)
    print(f"Pause/Unpause: {args.pause_unpause_bool}")
    print(f"Config Repo Path: {args.config_repo_path}")
    print(f"Source System: {args.source_system}")
    print(f"Pipeline: {args.pipeline}")
    print(f"Environment: {args.env}")
    print(f"Territory: {args.territory}")
    print(f"Table Names: {args.table_names}")
    print(f"Task Names: {args.task_names}")

    if args.pipeline == "gold" and not args.task_names:
        print("Error: task_names is required when pipeline is gold.")
        return

    if args.pipeline == "slilver" and not args.table_names:
        print("Error: table_names is required when pipeline is gold.")
        return

    if args.pipeline == "cmt" and not args.cmt_version:
        print("Error: cmt_version is a required argument when pipeline is cmt.")
        return

    if args.pipeline == "silver":
        print("\n🥈 Updating Silver pipelines\n")
        SilverConfig(
            args.config_repo_path, args.source_system, args.env, args.territory
        ).remove_table_entries(args.table_names)
    elif args.pipeline == "gold":
        print("\n🥇 Updating Gold pipelines\n")
        GoldConfig(
            args.config_repo_path, args.source_system, args.env, args.territory
        ).remove_tasks_from_workflow(args.task_names)
    elif args.pipeline == "cmt":
        print("\n🛠 Updating CMT pipelines\n")
        CMTConfig(
            args.config_repo_path, args.source_system, args.territory
        ).update_artifact_version(args.cmt_version)
    else:
        raise ValueError("Please check your input arguments.")


# if __name__ == '__main__':
#     main()

# remove_table_entries("../vitruvian-deployment-configurations/","excite","prod","na-us-pa",["compensation_v1"])
# goldconfig = GoldConfig("../vitruvian-deployment-configurations/","excite","int","na-us-nj")
# goldconfig.remove_tasks_from_workflow(["fct_compensation_event","fct_payment_event"])
# cmt_config = CMTConfig("../vitruvian-deployment-configurations/", "excite", "na-us-nj")
# cmt_config.update_artifact_version("1.0.524")

ENVS = ["int", "prod"]
TERRITORIES = ["na-us-nj", "na-us-pa", "na-ca-on", "eu"]


def run_all_silver(config_repo_path, source_system, table_names):
    print("\n🥈 Updating Silver pipelines\n")
    for env, territory in itertools.product(ENVS, TERRITORIES):
        print("\nFor: ", env, territory, "\n-------------")
        config = SilverConfig(config_repo_path, source_system, env, territory)
        config.remove_table_entries(table_names)


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
# run_all_cmt("../vitruvian-deployment-configurations/", "excite", "1.0.534")
