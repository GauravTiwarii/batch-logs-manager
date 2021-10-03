### **Batch Log Manager**

Processes CSV files uploaded to S3 bucket to Sqlite using Lambda.


To deploy **Batch Log Manager**, please follow the following steps :


1:` aws s3 mb s3://<bucket_name> --versioning-configuration Status=Enabled` [ note : This needs to be unique]

Navigate to lambda folder, where handler.py is present:

2. tar -caf ../../infra/lambda_zips/BatchLogManager.zip .

Navigate back to "batch-log-manager"

3. `aws s3api put-object --bucket lambda-zips-2021 --key BatchLogManager --body ./infra/lambda_zips/BatchLogManager.zip`

From the output of 3, extract the "VersionId" and put it as value for "`S3ObjectVersion`" in `./infra/resources.yml`

To deploy/update Stack, use the following command:
4. `aws cloudformation deploy --template-file ./infra/packaged-resources.yml --stack-name BatchLogManager --capabilities CAPABILITY_IAM`


_Note: Logs will be available under LogGroup "/aws/lambda/BatchLogManager" on CloudWatch_