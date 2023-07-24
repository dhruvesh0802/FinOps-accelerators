# File description: This python script will delete the EBS snapshots which are present in CSV file, you will need to provide the IDs of snapshot in CSV file. This CSV file is uploded on S3 bucket
# Author: dhruvesh.sheladiya@intuitive.cloud
# Date: 26/05/23
# Version: 2023.00.01
# Dependencies: csv, boto3

import csv
import boto3

s3 = boto3.resource('s3')
ec2 = boto3.resource('ec2')

bucket_name = "filtered_ebs_snapshot"
file_name = "snapshot/del_snapshots_ebs.csv"

def main():
    bucket = s3.Bucket(bucket_name)
    obj = bucket.Object(key=file_name)
    response = obj.get()
    csvfile = response['Body'].read().decode('utf-8').splitlines(True)
    csvReader = csv.reader(csvfile)
    #Iterating through the Snapshot ID from CSV file
    for lines in csvReader:
        lines = listToString(lines)
        snapshot = ec2.Snapshot(lines)
        #deleteing the snapshot
        snapshot.delete()

def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele
    # return string
    return str1

main()
