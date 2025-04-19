import json
import boto3
import uuid
import time
import os
import mimetypes
import base64

s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']
EXPIRY_TIME = 3600  # 1 hour in seconds

def lambda_handler(event, context):
    try:
        # Parse the request body
        body = json.loads(event['body'])
        file_content = body.get('file_content')
        file_name = body.get('file_name')
        
        if not file_content or not file_name:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Missing file content or file name'})
            }
        
        # Generate a unique code
        unique_code = str(uuid.uuid4())[:8]
        
        # Add metadata including timestamp for expiry check
        metadata = {
            'timestamp': str(int(time.time())),
            'original_filename': file_name
        }
        
        # Determine the content type based on file extension
        content_type, _ = mimetypes.guess_type(file_name)
        if content_type is None:
            content_type = 'application/octet-stream'  # Default if type cannot be determined
        
        # Decode the base64 content before uploading to S3
        try:
            decoded_content = base64.b64decode(file_content)
        except Exception as e:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Invalid file content encoding'})
            }
        
        # Upload to S3 with the unique code as part of the key
        s3_key = f"{unique_code}/{file_name}"
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=decoded_content,
            Metadata=metadata,
            ContentType=content_type
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'code': unique_code,
                'message': 'File uploaded successfully'
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }