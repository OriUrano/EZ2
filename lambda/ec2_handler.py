import json
import boto3
from botocore.exceptions import ClientError
import os

def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS'
    }
    
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        ec2_client = boto3.client('ec2', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
        
        response = ec2_client.describe_instances()
        
        instances = []
        
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instances.append({
                    'instanceId': instance.get('InstanceId'),
                    'instanceType': instance.get('InstanceType'),
                    'state': instance.get('State', {}).get('Name'),
                    'publicIpAddress': instance.get('PublicIpAddress'),
                    'privateIpAddress': instance.get('PrivateIpAddress'),
                    'launchTime': instance.get('LaunchTime').isoformat() if instance.get('LaunchTime') else None,
                    'tags': instance.get('Tags', []),
                    'availabilityZone': instance.get('Placement', {}).get('AvailabilityZone'),
                    'securityGroups': [
                        {
                            'groupId': sg.get('GroupId'),
                            'groupName': sg.get('GroupName')
                        }
                        for sg in instance.get('SecurityGroups', [])
                    ]
                })
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'instances': instances,
                'count': len(instances)
            })
        }
        
    except ClientError as e:
        print(f"AWS Error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Failed to fetch EC2 instances',
                'message': str(e)
            })
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }