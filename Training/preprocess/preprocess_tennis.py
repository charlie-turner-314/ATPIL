"""
Ensure before running this that 'process_hybrik_data.py' has been run on all hybrik results
The input should then be a directory that contains .pkl files
"""

import os
import joblib
import numpy as np
import argparse


def process_files(directory):
    """
    Finds the  files in the directory and processes them ready to train EmbodiedPose
    """
    result = {}
    num_success = 0
    for root, _, files in os.walk(directory):
        filenames = [os.path.join(root, f) for f in files]
        for file in filenames:
            if file.endswith("pkl"):
                with open(file, "rb") as f:
                    data = joblib.load(f)
                for m in data.keys():
                    if all(
                        key in data[m].keys()
                        for key in ["trans", "beta", "gender", "pose_aa"]
                    ):
                        result[f"file_{m}"] = {
                            "trans": data[m]["trans"],
                            "beta": data[m]["beta"],
                            "gender": data[m]["gender"],
                            "pose_aa": data[m]["pose_aa"],
                        }
                        num_success = num_success + 1

    print(f"Found {num_success} motions!")
    return result


def save_results(results, out_path):
    with open(out_path, "wb") as f:
        joblib.dump(results, f)
    print("Saved results to", out_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", help="path/to/tennis_data", required=True)
    parser.add_argument("--output", help="path/to/processed_data.pkl", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        print(f"Argument --input_dir={args.input_dir} does not exist")
        exit(1)
    if not os.path.exists(os.path.dirname(args.output)):
        print(f"Containing folder of --output={args.output} does not exist")
        exit(1)

    results = process_files(args.input_dir)
    save_results(results, args.output)
