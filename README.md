# EZ2 - EC2 Dashboard

A modern, responsive dashboard for monitoring AWS EC2 instances built with SvelteKit and Tailwind CSS.

## Features

- **Real-time EC2 monitoring** - View all your EC2 instances with current status
- **Instance details** - See instance type, IP addresses, availability zones, and launch times
- **Status indicators** - Color-coded status badges for quick instance state identification
- **Responsive design** - Works seamlessly on desktop and mobile devices
- **Serverless backend** - Uses AWS Lambda with Function URLs for data fetching
- **Static site generation** - Can be deployed as a static site to any hosting provider

## Architecture

- **Frontend**: SvelteKit with Tailwind CSS
- **Backend**: AWS Lambda function (Python) with Function URL
- **Deployment**: Static site generation with serverless API

## Setup

### Prerequisites

- Node.js 18+ and npm
- AWS account with EC2 access
- AWS CLI configured (for Lambda deployment)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/OriUrano/EZ2.git
cd EZ2
```

2. Install dependencies:
```bash
npm install
```

3. Deploy the Lambda function:
```bash
# Create a Lambda function with the code from lambda/ec2_handler.py
# Set up Function URL with CORS enabled
# Apply the required IAM permissions (see Lambda Setup section)
```

4. Start the development server:
```bash
npm run dev
```

### Lambda Setup

1. Create a Lambda function with Python 3.9 runtime
2. Upload the code from `lambda/ec2_handler.py`
3. Create a Function URL with CORS enabled
4. Apply IAM role with these permissions:
   - `AWSLambdaBasicExecutionRole` (managed policy)
   - Custom policy for EC2 read access:
     ```json
     {
         "Version": "2012-10-17",
         "Statement": [
             {
                 "Effect": "Allow",
                 "Action": [
                     "ec2:DescribeInstances",
                     "ec2:DescribeInstanceStatus"
                 ],
                 "Resource": "*"
             }
         ]
     }
     ```

### Configuration

1. Open the dashboard in your browser
2. Enter your Lambda Function URL in the configuration section
3. Click "Save & Fetch" to start monitoring your instances

## Development

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm run test

# Format code
npm run format

# Lint code
npm run lint
```

## Deployment

The dashboard can be deployed as a static site to any hosting provider:

```bash
npm run build
```

Deploy the `build` directory to your hosting provider of choice (Vercel, Netlify, AWS S3, etc.).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request
