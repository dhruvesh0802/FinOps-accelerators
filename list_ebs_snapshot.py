# File description: This python script will list the EBS snapshots which are "x" days older and store it in csv file that will be uploded to S3 bucket
# Author: harsh.viradia@intuitive.cloud, dhruvesh.sheladiya@intuitive.cloud and jay.sheth@intuitive.cloud
# Date: 26/05/23
# Version: 2023.00.01
# Dependencies: csv, boto3, datetime

import boto3
import csv
from datetime import datetime, timedelta, timezone

ec2 = boto3.resource('ec2')
s3 = boto3.client("s3")
snapshots = ec2.snapshots.filter(OwnerIds=['self'])

fields = ['SnapshotID', 'VolumeID', 'Volume Size', 'Encryption', 'Start Time', 'Delete Time']
result = []

x = input("Enter x number of days: ")

#iterate over all the snapshots
for snapshot in snapshots:
    start_time = snapshot.start_time
    delete_time = datetime.now(tz=timezone.utc) - timedelta(days=x)

    #checking the condition
    if delete_time > start_time:
        print('fmt_start_time = {} and delete_time = {}' .format(start_time,delete_time))
        sub_result = [snapshot.snapshot_id, snapshot.volume_id, snapshot.volume_size, snapshot.encrypted, start_time, delete_time]
        result.insert(0, sub_result)

    #storing the snaoshots data in csv file
    with open("/tmp/old_snapshots_ebs.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(result)

    #uploading on to s3
    response = s3.upload_file('/tmp/old_snapshots_ebs.csv', 'filtered_ebs_snapshot', 'snapshot/old_snapshots_ebs.csv')
