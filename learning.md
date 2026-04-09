Hello!!! This file is just for the stuff I learned from this project fun
🥹 my baby project is all grown up


- S3 Bucket = is a top level conatiner for files (called "objects")
    -Contrary to the name everything sits at the same level there is no file structure within a bucket (No nested folders or files)
    -Bucket Names are Globally unique for all AWS
    -name: workbud-photos-holden, region: us-east-2

-IAM: AWS permission system. everything that interacts with AWS needs an indentity that defines what it can do. 

-NEVER USE ROOT CREDENTIALS IN CODE; If leaked hacker owns your whole AWS account basically
    -Make a dedicated IAM user for the FastAPI that only lets it interact with the S3 bucket that way if leaked they only have access to the bucket 

-Least Priveledge: Basically everything gets the least amount of priveldges neededto do its job. Security idea so the least amount of stuff breaks