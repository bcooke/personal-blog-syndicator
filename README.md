# 🚀 Blog Syndicator for LinkedIn and Twitter

This AWS SAM application automates the process of syndicating blog posts to LinkedIn and Twitter. It uses AWS Lambda to check for new posts in an RSS feed and then posts these updates to your social media accounts.

## 📋 Features

- **Automated Social Media Posting**: Posts new blog entries to LinkedIn and Twitter automatically.
- **Serverless Architecture**: Built on AWS Lambda for efficient, on-demand processing.
- **Secure Credential Management**: Utilizes AWS Secrets Manager for secure storage of API credentials.
- **Customizable Posting Schedule**: Schedule can be easily adjusted to suit your needs.

## 🛠️ Setup and Configuration

### Prerequisites

- An AWS account with appropriate permissions.
- LinkedIn and Twitter developer accounts and created apps.
- AWS CLI and AWS SAM CLI installed.
- Basic knowledge of AWS services like Lambda, Secrets Manager, and IAM.

### Initial Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/bcooke/personal-blog-syndicator
   cd personal-blog-syndicator
   ```

2. **Setup Developer Accounts and Apps:**
- Create LinkedIn and Twitter developer accounts.
- Setup applications on both platforms to get API credentials.

3. **Store Credentials in AWS Secrets Manager:**
- Store the obtained API credentials securely in AWS Secrets Manager.
Note the ARNs (Amazon Resource Names) of these secrets.

4. **Configure IAM Roles:**
- Ensure your IAM access is configured for all the AWS resoures you'll be using

5. **Update .env file:**
- Use the .env.example as a template to create a .env file.
- Fill in the ARNs of your secrets in the .env file.


### Deployment

To deploy the application, use the deploy.sh script located in ./scripts directory to deploy your application.
```bash
./scripts/deploy.sh
```

## 📝 Usage
- The application will automatically check the RSS feed and post updates according to the defined schedule in the SAM template.
- For local testing of Lambda functions:
-- Use ./scripts/test_linkedin.sh for testing the LinkedIn posting function.
-- Use ./scripts/test_twitter.sh for testing the Twitter posting function.

## 🔧 Development and Contribution
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature.
3. Implement your feature or fix and test it.
4. Submit a pull request with a comprehensive description of your changes.

## 🤝 Issues and Suggestions
If you encounter any issues or have suggestions, feel free to open an issue on the GitHub repository.

## 🌟 Show Your Support
Give a ⭐️ if you find this project useful!

## 📄 License
This project is open-source and available under the MIT License.

## ✍️ Authors
- Brett Cooke @bcooke