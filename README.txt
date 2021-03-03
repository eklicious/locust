1. create a .dockerignore file and ignore the __pycache__
2. create a dockerfile
   a. In the docker file, make sure to RUN pip install -r requirements.txt
3. build a custom image (https://stackify.com/docker-build-a-beginners-guide-to-building-docker-images/), e.g. docker build -t ek/locust-test .
   a. Need to push our custom images to dockerhub or elastic container registry
4. Running locust
   a. locally with no container, e.g. locust
   b. locally with a container, e.g. docker run -p 8089:8089 -v $PWD:/mnt/locust ek/locust-test -f /mnt/locust/locustfile.py
   c. locally with docker-compose, e.g. docker compose up
   d. on ecs (https://docs.docker.com/engine/context/ecs-integration/)
      i. Create an aws iam policy (named locust_ecs) for given aws user, e.g.

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "elasticfilesystem:*",
                "iam:*",
                "servicediscovery:*",
                "application-autoscaling:*",
                "logs:*",
                "route53:*",
                "ecs:*",
                "ecr:*",
                "ec2:*",
                "cloudformation:*",
                "elasticloadbalancing:*"
            ],
            "Resource": "*"
        }
    ]
}

      ii. Create Security credentials > Create access key for aws login
      iii. Create a private ECR repo, e.g. locust
      iv. view local docker images and grab the id, e.g. docker images
      v. tag the docker image to ECR, e.g. docker tag 1b8b1ac0b63e 005879814094.dkr.ecr.us-east-1.amazonaws.com/locust
      vi. Install aws cli, https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html
      vii. Get the password, (aws ecr get-login-password --region us-east-1)
      viii. log into ecr, e.g. docker login -u AWS -p <password from the step above> https://005879814094.dkr.ecr.us-east-1.amazonaws.com
      ix. push the docker image to ecr, e.g. docker push 005879814094.dkr.ecr.us-east-1.amazonaws.com/locust:latest
      x. Create a docker ecs context, e.g. docker context create ecs ecscontext

d? Create a Docker context using: AWS secret and token credentials
Retrieve or create AWS Access Key and Secret on https://console.aws.amazon.com/iam/home?#security_credential
? AWS Access Key ID AKIAQCXTW27HDZN3H75G
? Enter AWS Secret Access Key ****************************************
? Region us-east-1
Successfully created ecs context "ecscontext"

      xi. Verify the context was created, e.g. docker context ls
      xii. Update the docker compose x-aws-vpc to use an existing vpc in case if you are running ec2 classic. I think you need to make sure the vpc has DNS host enabled. There seems to be a bug with mounting NFS so I had to hard code the NFS file system id after running docker compose up to warm up NFS.
      xiii. run docker compose with proper ecs context, e.g. docker compose up --context ecscontext
      xiv. find the ec2 load balancer address and use browser for <load balancer external address>:8089
      xv. Tear down docker compose using docker compose down --context ecscontext
