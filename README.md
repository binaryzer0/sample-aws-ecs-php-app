
# Welcome to your sample-aws-ecs-php-app CDK Python project!

This is a sample code to deploy a PHP Application using AWS ECS and CDK

PHP Code directory: ./sample_aws_ecs_php_app/php-app/src/
Docker file: ./sample_aws_ecs_php_app/php-app/Dockerfile

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

We also need following system enviornment variables defined to make the stack work:

CDK_DEFAULT_ACCOUNT - Default AWS account # where application is being deployed
CDK_DEFAULT_REGION - Default region where application is being deployed


```
export CDK_DEFAULT_ACCOUNT=XXXX
export CDK_DEFAULT_REGION=XXXX
```

Optional (only used if deploying SSL based application along with Route53 Public Hosted Zone + AWS Certificate Manager)

CDK_DOMAIN_NAME - Domain name for Route53 Public Hosted Zone.
CDK_FQDN - Domain name to be used for Application behind the Load Balancer e.g. crypto-sheriff.nomoreransom.org
CDK_CERT_ARN - ARN # from AWS Certificate Manager to be used with the application load balancer

```
export CDK_DOMAIN_NAME="XXXX"
export CDK_FQDN="XXXX"
export CDK_CERT_ARN="XXXX"
```

Install CDK Toolkit stack which allows to stage assets such as Docker images

```cdk bootstrap aws://ACCOUNT-NUMBER-1/REGION-1 aws://ACCOUNT-NUMBER-2/REGION-2 ...```


At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

Once Synth process is complete - you are ready to Deploy.

```
cdk deploy
```

Enjoy!

