import boto3
import time
import os
import botocore
import json
from botocore.exceptions import ClientError
from botocore.client import Config
import urllib.parse

def lambda_handler (event, context):
  for record in event.get('Records'):
    print('Received event: ' + json.dumps(event))
    if record.get('eventName') == 'MODIFY':
      if record['dynamodb']['OldImage']['audioFromCustomer']['S'] == '':
        contact_id = record['dynamodb']['NewImage']['contactId']['S']
        customer_phone_number = record['dynamodb']['NewImage']['customerPhoneNumber']['S']
        vm_audio = record['dynamodb']['NewImage']['audioFromCustomer']['S']

        try:
          task_client = boto3.client('connect')
          response = task_client.start_task_contact(
          InstanceId = os.environ.get('InstanceId'),
          PreviousContactId = contact_id,
          ContactFlowId = os.environ.get('ContactFlowId'),
          Attributes= {
          'Phone_Number': customer_phone_number
          },
          References={
          'Voicemail': {'Value': vm_audio , 'Type': 'URL'}
          },
          Name = "New Voicemail",
          Description= 'A caller has left a new voicemail',
          )
        except ClientError as e:
          print(e.response['Error']['Message'])
        else:
          print("Task created"),
          #print(response)
