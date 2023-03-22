import argparse
import os
import numpy as np
import cv2
from azureml.core import Run
from azureml.pipeline.core import PipelineData
from azureml.core import Datastore
from azureml.core import Workspace
from datetime import datetime
from azureml.core import Dataset
import json 

parser = argparse.ArgumentParser()
parser.add_argument('--output_path', type=str, help='output path')
parser.add_argument('--blob_datastore_name', type=str, help='output path')
parser.add_argument('--blob_container_name', type=str, help='output path')
parser.add_argument('--blob_account_name', type=str, help='output path')
parser.add_argument('--blob_account_key', type=str, help='output path')
parser.add_argument('--datadir', type=str, required=True)

args = parser.parse_args()
print("Argument 1: %s" % args.output_path)
print("Argument 2: %s" % args.blob_datastore_name)
print("Argument 3: %s" % args.blob_container_name)
print("Argument 4: %s" % args.blob_account_name)
print("Argument 5: %s" % args.blob_account_key)

run = Run.get_context()
ws = run.experiment.workspace
blob_datastore = Datastore.register_azure_blob_container(workspace=ws, 
                                                         datastore_name=args.blob_datastore_name, 
                                                         container_name=args.blob_container_name, 
                                                         account_name=args.blob_account_name,
                                                         account_key=args.blob_account_key)

if not (args.output_path is None):
    os.makedirs(args.output_path, exist_ok=True)
    print("%s created" % args.output_path)

json_file = open(os.path.join(args.datadir, "Step1-Parameter.json"))
datas = json.load(json_file)
json_file.close()
print(f"lastestCsvName: {datas['lastestCsvName']}")
with open(os.path.join(args.output_path, f"Step2-Output-{datas['lastestCsvName']}.txt"), 'w') as text_file:
    print("Created Output.txt Finished - Hello World")
    text_file.write(f"Hello World")
    print("Created Output.txt Finished")

blob_datastore.upload_files([
    os.path.join(args.output_path, f"Step2-Output-{datas['lastestCsvName']}.txt")
], target_path='Image', overwrite=True)
