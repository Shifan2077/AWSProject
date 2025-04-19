**Methodology**
The implementation of Secure File Share follows these steps:
Create an S3 Bucket:
A dedicated Amazon S3 bucket was created to store user-uploaded files.
Configured Bucket Policies to ensure only authorized users and services can access files.
Set Up IAM Roles:
Created an IAM role to allow AWS Lambda to interact with the S3 bucket.
Assigned least-privilege permissions to restrict access only to necessary actions.
Develop AWS Lambda Functions:
Upload Function: Receives file data and saves it in S3.
Download Function: Retrieves requested files from S3.
Cleanup Function: Deletes uploaded files after 3 minutes using Amazon CloudWatch Scheduled Events.

Cleanup Function:
Scheduled via AWS EventBridge (CloudWatch Scheduled Events).
Automatically runs every minute.
Scans files in the S3 bucket.
Deletes files that are older than 3 minutes to maintain security and reduce storage usage.
Frontend Development:
Built a web interface using HTML, CSS, and JavaScript.
Integrated API Gateway to communicate with AWS Lambda functions.
Testing & Deployment:
Deployed the web application.
Tested file upload, download, and cleanup operations.



**Implementation**
 Setting Up Amazon S3 Bucket
Step 1: Logging into AWS Management Console
Logged into AWS Management Console at AWS Console.
Navigated to the Amazon S3 service.


Step 2: Creating a New S3 Bucket
Clicked on "Create bucket" in the S3 dashboard.
Provided a unique bucket name, e.g., file-sharing-app-b1.
Selected the preferred AWS region to optimize latency and availability.


Step 3: Configuring Permissions to Restrict Access
Set the "Block all public access" option to ensure files are private.
Configured bucket policies to allow only authorized IAM roles and AWS Lambda functions to access the bucket.


🔹 Screenshot 1: S3 Bucket Creation


 🔹 Screenshot 2: S3 Bucket Permissions Configuration

Configuring IAM Roles for AWS Lambda
IAM (Identity and Access Management) roles control access to AWS services, ensuring that only authorized functions interact with S3.
Step 1: Creating an IAM Role for AWS Lambda
Navigated to the IAM Dashboard and selected "Roles" → "Create Role".
Chose AWS Service → Lambda as the trusted entity.
Assigned the necessary permissions for Lambda to interact with S3.
Step 2: Assigning IAM Policies to the Role
Created a new IAM policy with the following permissions:
s3:PutObject → Allows uploading files to S3.
s3:GetObject → Allows downloading files from S3.
s3:DeleteObject → Allows deleting files after 3 minutes.
s3:ListBucket → Allows scanning the bucket for cleanup.


Attached this policy to the IAM Role (LambdaS3AccessRole).
Step 3: Attaching the IAM Role to Lambda
While configuring AWS Lambda functions, attach the IAM Role to grant necessary access.
🔹 Screenshot 3: IAM Role Creation



Developing AWS Lambda Functions
AWS Lambda is used to handle file uploads, downloads, and automatic cleanup without requiring a dedicated server.
Purpose:
Receives a file from the user via a web request.
Stores the file securely in the Amazon S3 bucket.
Generates a unique file name to avoid conflicts.
Implementation Steps:
Created a new AWS Lambda function in the AWS Lambda Console.
Selected Python 3.x as the runtime environment.
Wrote a function using boto3 (AWS SDK for Python) to upload files to S3.
Configured API Gateway to trigger this function via HTTP requests.
Tested the function by uploading a sample file and verifying storage in S3.
