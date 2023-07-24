# File description: This python script Listout EBS volume which are attached to EC2 whose state is stooped. And it will create CSV file and uploaded to S3 bucket.
# Author: dhruvesh.sheladiya@intuitive.cloud
# Date: 26/05/23
# Version: 2023.00.01
# Dependencies: csv, boto3

import boto3
import csv

# create a session using the default AWS credentials
session = boto3.Session()

fields = ['SnapshotID', 'VolumeID']
result = []

# create an EC2 resource and s3 client
ec2_resource = session.resource('ec2')
s3 = boto3.client("s3")

# use the volumes attribute to get a list of all EBS volumes
volumes = ec2_resource.volumes.all()

# use the instances attribute to get a list of all EC2 instances
instances = ec2_resource.instances.all()

# loop through the instances and check their state to determine if they are stopped
for instance in instances:
    if instance.state['Name'] == 'stopped':
        print(instance.id)
        for volume in instance.volumes.all():
            if volume.state == 'in-use':
                print(volume.id)
                sub_result = [instance.id, volume.id]
                result.insert(0, sub_result)


# create CSV file and upload it on a S3 bucket.
with open("/tmp/old_snapshots_ebs.csv", 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(result) 

response = s3.upload_file('/tmp/ebs_volume_list.csv', 'ebs_volume_list', 'snapshot/ebs_volume_list.csv')
