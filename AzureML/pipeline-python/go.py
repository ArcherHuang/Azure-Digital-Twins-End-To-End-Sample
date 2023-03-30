import argparse
import os
import numpy as np
import cv2
import pandas as pd
from azureml.core import Run
from azureml.pipeline.core import PipelineData
from azureml.core import Datastore
from azureml.core import Workspace
from datetime import datetime
import glob
import os.path
from azureml.core import Dataset
import json

parser = argparse.ArgumentParser()
parser.add_argument('--output_path', type=str, help='output path')
parser.add_argument('--blob_datastore_name', type=str, help='output path')
parser.add_argument('--blob_container_name', type=str, help='output path')
parser.add_argument('--blob_account_name', type=str, help='output path')
parser.add_argument('--blob_account_key', type=str, help='output path')

args = parser.parse_args()
print(f"Argument 1: {args.output_path}")
print(f"Argument 2: {args.blob_datastore_name}")
print(f"Argument 3: {args.blob_container_name}")
print(f"Argument 4: {args.blob_account_name}")
print(f"Argument 5: {args.blob_account_key}")

if not (args.output_path is None):
    os.makedirs(args.output_path, exist_ok=True)
    print(f"{args.output_path} created")
else:
    print(f"output path : {args.output_path}")    

run = Run.get_context()
ws = run.experiment.workspace
blob_datastore = Datastore.register_azure_blob_container(workspace=ws, 
                                                         datastore_name=args.blob_datastore_name, 
                                                         container_name=args.blob_container_name, 
                                                         account_name=args.blob_account_name,
                                                         account_key=args.blob_account_key)

files = Dataset.File.from_files((blob_datastore, 'Report/**'))
print(f"files: {files}")
csv_files = files.to_path()
print(f"csv_files path: {csv_files}")

datetimes = [datetime.strptime(filename[1:-4], '%Y%m%d-%H%M%S') for filename in csv_files]
sorted_datetimes = sorted(datetimes, reverse=True)
sorted_csvs = ['/' + datetime.strftime(dt, '%Y%m%d-%H%M%S') + '.csv' for dt in sorted_datetimes]
latest = sorted_csvs[0]
latest_csv_file = latest.replace('/', '').split('.')[0]
print(f"Argument 7: {latest_csv_file}")

path = f"https://{args.blob_account_name}.blob.core.windows.net/adt/Report/"
file = f"{path}{latest_csv_file}.csv"

# Construct a empty image of wafer
height = 300*2   # 5 pixels/mm
width = 400*2
waferimage = np.zeros(shape=[height, width, 3], dtype=np.uint8)
# Center coordinates
center_coordinates = (300, 300)  
# Radius of circle
radius = 300   
# Blue color in BGR
color = (255, 255, 255)
# Line thickness of 2 px
thickness = 2
# Draw a circle with blue line borders of thickness of 2 px
waferimage = cv2.circle(waferimage, center_coordinates, radius, color, thickness)
      
data = pd.read_csv(file, header=0, usecols=['Film Thickness 1', 'Film Thickness 2', 'X', 'Y'])  
print(f"T0 : {data['Film Thickness 1'][0]}")
print(f"T1 : {data['Film Thickness 1'][1]}")
print(f"Tsd : {data['Film Thickness 2'][len(data.index)-6]}")
print(f"Taverage : {data['Film Thickness 2'][len(data.index)-5]}")
print(f"Tuniformity : {data['Film Thickness 2'][len(data.index)-4]}")
print(f"TMax : {data['Film Thickness 2'][len(data.index)-3]}")
print(f"TMin : {data['Film Thickness 2'][len(data.index)-2]}")

Tsd = int(data['Film Thickness 2'][len(data.index)-6])
Taverage = int(data['Film Thickness 2'][len(data.index)-5])
Tuniformity = int(data['Film Thickness 2'][len(data.index)-4])
TMax = int(data['Film Thickness 2'][len(data.index)-3])
TMin = int(data['Film Thickness 2'][len(data.index)-2])
# Draw the colorbar
colorx = 680
xstep = 50
colory = 550 
ystep = 1
level = 0
cv2.putText(waferimage, "0", (colorx+xstep+10, colory), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
for ci in range(0, 540): 
    level = level + 31060
    cB = int(level&0x000000FF)
    cG = int(level&0x0000FF00)>>8
    cR = int(level&0x00FF0000)>>16 
               
    cX = colorx
    cY = colory - ystep * (ci+1)     
    cv2.rectangle(waferimage, (cX,cY), (cX+xstep,cY+ystep), (cB,cG,cR), -1)
    if ci % 540 == 135 or ci % 540 == 270 or ci % 540 == 405:
        cv2.putText(waferimage, f"{level}", (colorx+xstep+5,cY), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255,255,255), 1, cv2.LINE_AA)

cv2.rectangle(waferimage, (colorx,colory-540), (colorx+50,colory), (255,255,255), 1, cv2.LINE_AA)
cv2.putText(waferimage, "16,777,216", (colorx+xstep+5, colory-540), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255,255,255), 1, cv2.LINE_AA)
# Put data informations on image
cv2.putText(waferimage, f"Average = {Taverage}", (500,540), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255,255,255), 1, cv2.LINE_AA)
cv2.putText(waferimage, f"Uniformity = {Tuniformity}%", (500,555), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255,255,255), 1, cv2.LINE_AA)
cv2.putText(waferimage, f"Max = {TMax}", (500,570), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255,255,255), 1, cv2.LINE_AA)
cv2.putText(waferimage, f"Min = {TMin}", (500,585), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255,255,255), 1, cv2.LINE_AA)

count = 0
defectTable = []
defectX = []
defectY = []
defectT = []
# iterate through excel and display data 
for i in range(0, len(data.index)-7):
    #print('\n')
    #print('Row ', i, 'Data :')
      
    # col#1 (thickness (A)), col#5 X (mm), col#6 Y (mm), 
    thickness = int(float(data['Film Thickness 1'][i]))
    B1 = int(thickness&0x000000FF)
    G2 = int(thickness&0x0000FF00)>>8
    R3 = int(thickness&0x00FF0000)>>16 
    #print(thickness, B1, G2, R3)
    X = ( int(data['X'][i]) + 150 ) * 2
    Y = (- int(data['Y'][i]) + 150 ) * 2
    #print('X = %d, Y = %d' %(X,Y))  
    if thickness > (Taverage + Tsd) or thickness < (Taverage - Tsd):
        count = count + 1
        defectTable.append([X, Y, thickness])
        defectX.append(X)
        defectY.append(Y)
        defectT.append(thickness)

    cv2.rectangle(waferimage, (X-10,Y-10), (X+10,Y+10), (B1,G2,R3), -1)
    #waferimage[X,Y] = (B1,G2,R3)

print(f"defect count : {count}")
print(f"defect Table : {defectTable}")
run.log("[Data Tracking] defect count :", count)

logtable = {
        'X (mm)': defectX,
        'Y (mm)': defectY,
        'Thickness (A)': defectT
    }
run.log_table("Data Tracking", logtable)

cv2.imwrite(f"outputs/{latest_csv_file}.png", waferimage)
blob_datastore.upload_files([
    f"outputs/{latest_csv_file}.png"
], target_path='Image', overwrite=True)
run.log_image("Thinfilm on wafer", f"outputs/{latest_csv_file}.png")