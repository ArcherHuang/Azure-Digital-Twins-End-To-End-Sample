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
parser.add_argument('--output_folder', dest='output_folder', required=True)

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

files = Dataset.File.from_files((blob_datastore, 'Report/**'))
print(f'files: {files}')
csv_files = files.to_path()
print(f'csv_files path: {csv_files}')

datetimes = [datetime.strptime(filename[1:-4], '%Y%m%d-%H%M%S') for filename in csv_files]
sorted_datetimes = sorted(datetimes, reverse=True)
sorted_csvs = ['/' + datetime.strftime(dt, '%Y%m%d-%H%M%S') + '.csv' for dt in sorted_datetimes]
latest = sorted_csvs[0]
latest_csv_file = latest.replace('/', '').split('.')[0]
print("Argument 7: %s" % latest_csv_file)

run.log('Step', '[Step1] create_png.py')
run.log('最新的 csv 檔名', latest_csv_file)

if not (args.output_path is None):
    os.makedirs(args.output_path, exist_ok=True)
    print("%s created" % args.output_path)

parameter_json = {
    "lastestCsvName": latest_csv_file
}

with open(os.path.join(args.output_folder, "Step1-Parameter.json"), 'w') as outfile:
    print(f"Created {latest_csv_file}")
    json.dump(parameter_json, outfile)

rgb = np.random.randint(255, size=(900, 800, 3), dtype=np.uint8)
cv2.imwrite(os.path.join(args.output_path, f"Step1-Image-{latest_csv_file}.png"), rgb)

blob_datastore.upload_files([
    os.path.join(args.output_path, f"Step1-Image-{latest_csv_file}.png")
], target_path='Image', overwrite=True)
