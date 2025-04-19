Secure File Share is a lightweight, serverless file-sharing web application hosted on Amazon Web Services (AWS). It allows users to upload and share files temporarily with automatic deletion after 3 minutes. Built using Amazon S3, AWS Lambda, and IAM Roles, this project demonstrates the power of cloud-native tools in building secure, scalable, and cost-effective solutions.

**🚀 Features**
Upload and share files securely via unique links

Files are automatically deleted 3 minutes after upload

Completely serverless — no backend server to manage

Built with AWS Free Tier in mind

Uses IAM Roles for secure access to AWS resources

🛠️ Tech Stack
Frontend: HTML, CSS, JavaScript

Backend: AWS Lambda (Node.js / Python)

Storage: Amazon S3

Security: AWS IAM Roles

Hosting: AWS S3 + Lambda (serverless)

**🧩 How It Works**
User uploads a file via the web interface.

A Lambda function stores the file in an S3 bucket.

A unique link is generated for file download.

A separate Lambda function automatically deletes files 3 minutes after upload.

📂 Folder Structure
secure-file-share/
├── frontend/
│   └── index.html, script.js, style.css
├── lambda/
│   └── upload.js, download.js, cleanup.js
├── README.md
└── template.yaml (for AWS SAM if used)


**🛡️ Security**
This project uses AWS IAM Roles to strictly control access to file operations. Only authorized Lambda functions can read/write/delete files from the S3 bucket.

**✅ Deployment**
You can deploy this project using the AWS Management Console or Infrastructure as Code (e.g., AWS SAM or CloudFormation).
