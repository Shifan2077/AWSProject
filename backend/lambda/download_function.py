import json
import boto3
import os
import base64
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        # Parse the request
        code = event['queryStringParameters'].get('code')
        
        if not code:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET',
                    'Content-Security-Policy': "default-src 'self'",
                    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
                    'X-Content-Type-Options': 'nosniff'
                },
                'body': json.dumps({'error': 'Missing code parameter'})
            }
        
        # List objects with this prefix to find the file
        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=f"{code}/"
        )
        
        if 'Contents' not in response or len(response['Contents']) == 0:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET',
                    'Content-Security-Policy': "default-src 'self'",
                    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
                    'X-Content-Type-Options': 'nosniff'
                },
                'body': json.dumps({'error': 'File not found or code is invalid'})
            }
        
        # Get the first file matching the code prefix
        file_key = response['Contents'][0]['Key']
        
        # Get the file metadata and content
        obj_response = s3_client.get_object(
            Bucket=BUCKET_NAME,
            Key=file_key
        )
        
        # Get original filename from metadata
        original_filename = obj_response['Metadata'].get('original_filename', 'downloaded_file')
        
        # Get file content
        file_content = obj_response['Body'].read()
        
        # Get the content type from the object metadata
        content_type = obj_response.get('ContentType', 'application/octet-stream')
        
        # Base64 encode the file content for API Gateway response
        file_content_b64 = base64.b64encode(file_content).decode('utf-8')
        
        # Set secure headers for the response
        headers = {
            'Content-Type': content_type,
            'Content-Disposition': f'attachment; filename="{original_filename}"',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'X-Content-Type-Options': 'nosniff',
            'Content-Security-Policy': "default-src 'self' blob: data:",
            'X-Frame-Options': 'DENY'
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': file_content_b64,
            'isBase64Encoded': True
        }
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET',
                    'Content-Security-Policy': "default-src 'self'",
                    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
                    'X-Content-Type-Options': 'nosniff'
                },
                'body': json.dumps({'error': 'File not found'})
            }
        else:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET',
                    'Content-Security-Policy': "default-src 'self'",
                    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
                    'X-Content-Type-Options': 'nosniff'
                },
                'body': json.dumps({'error': str(e)})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Content-Security-Policy': "default-src 'self'",
                'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
                'X-Content-Type-Options': 'nosniff'
            },
            'body': json.dumps({'error': str(e)})
        }