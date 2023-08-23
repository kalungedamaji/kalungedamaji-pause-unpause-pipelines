import argparse
import os

from config_processors.cmt_config import CMTConfig
from config_processors.gold_config import GoldConfig
from config_processors.silver_config import SilverConfig


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


os.makedirs("paused", exist_ok=True)


if __name__ == "__main__":
    main()
