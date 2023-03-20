import argparse
import os
import numpy as np
import cv2
from azureml.core import Run
from azureml.pipeline.core import PipelineData
from azureml.core import Datastore
from azureml.core import Workspace
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--output_path', type=str, help='output path')
parser.add_argument('--blob_datastore_name', type=str, help='output path')
parser.add_argument('--blob_container_name', type=str, help='output path')
parser.add_argument('--blob_account_name', type=str, help='output path')
parser.add_argument('--blob_account_key', type=str, help='output path')
args = parser.parse_args()
print("Argument 1: %s" % args.output_path)
print("Argument 2: %s" % args.blob_datastore_name)
print("Argument 3: %s" % args.blob_container_name)
print("Argument 4: %s" % args.blob_account_name)
print("Argument 5: %s" % args.blob_account_key)

if not (args.output_path is None):
    os.makedirs(args.output_path, exist_ok=True)
    print("%s created" % args.output_path)

current_dateTime = datetime.now().strftime("%Y%m%d-%H%M%S")

rgb = np.random.randint(255, size=(900, 800, 3), dtype=np.uint8)
cv2.imwrite(os.path.join(args.output_path, f"Image-{current_dateTime}.png"), rgb)

with open(os.path.join(args.output_path, f"Output-{current_dateTime}.txt"), 'w') as text_file:
    print("Created Output.txt Finished - Hello World")
    text_file.write(f"Hello World")

print("Created Output.txt Finished")

run = Run.get_context()
ws = run.experiment.workspace
blob_datastore = Datastore.register_azure_blob_container(workspace=ws, 
                                                         datastore_name=args.blob_datastore_name, 
                                                         container_name=args.blob_container_name, 
                                                         account_name=args.blob_account_name,
                                                         account_key=args.blob_account_key)

blob_datastore.upload_files([
    os.path.join(args.output_path, f"Image-{current_dateTime}.png"),
    os.path.join(args.output_path, f"Output-{current_dateTime}.txt")
], target_path='Image', overwrite=True)
