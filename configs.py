import argparse

parser = argparse.ArgumentParser(description="implementation of mmkg")
parser.add_argument('--dataset_dir', type=str, default="")
parser.add_argument('--mode', type=str, default="Online Vision-needed", choices=["all", "Direct Vision-needed", "Direct", "Perfect", "self Search", "Offline", "Online Vision-needed"],
                    help='the order (Direct Vision-needed to Online Vision-needed) corresponding to the experiment setting in the ICCV 2025 paper.')
parser.add_argument('--model_name', type=str, default="gpt-4o-2024-11-20")
parser.add_argument('--api_key', type=str, default="")
parser.add_argument('--use_name', type=bool, default=True, help='whether use monster name for input query.')
parser.add_argument('--use_extra', type=bool, default=True, help='whether use extra data for input query.')