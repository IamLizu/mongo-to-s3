import os
import sys
from datetime import datetime
import subprocess
import shutil
from string import Template


def main():
    try:
        # Get the Python executable path
        python_executable = sys.executable

        # Create the logs directory if it doesn't exist
        logs_dir = os.path.expanduser("~/mongo-to-s3-logs")
        os.makedirs(logs_dir, exist_ok=True)

        # Define the backup location
        BACKUP_DIR = os.path.expanduser("~/mongo-to-s3-backups")
        os.makedirs(BACKUP_DIR, exist_ok=True)

        # Define the template script
        template = Template("""
import os
import boto3
from datetime import datetime
import logging

# Configure the logging
log_file = "$log_file"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Define the backup location
BACKUP_DIR = "$backup_dir"

# Define the database information
DB_HOST = "$db_host"
DB_PORT = $db_port
DB_NAME = "$db_name"
DB_USER = "$db_user"
DB_PASS = "$db_pass"

# Define the S3 bucket details
S3_BUCKET_NAME = "$s3_bucket_name"
S3_FOLDER_NAME = "$s3_folder_name"
S3_ACCESS_KEY = "$s3_access_key"
S3_SECRET_KEY = "$s3_secret_key"
S3_REGION = "$s3_region"

# Generate a timestamp for the backup file
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Create the backup
backup_dir = os.path.join(BACKUP_DIR, timestamp)
os.makedirs(backup_dir, exist_ok=True)
os.system(
    f"mongodump -u {DB_USER} -d {DB_NAME} -p {DB_PASS} --out {backup_dir}"
)

# Compress the backup file
backup_file = os.path.join(BACKUP_DIR, f"{timestamp}.tar.gz")
os.system(f"tar -zcvf {backup_file} {backup_dir}")

# Remove the uncompressed backup directory
os.system(f"rm -rf {backup_dir}")

# Upload the backup file to S3
try:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        region_name=S3_REGION,
    )
    s3_object_key = f"{S3_FOLDER_NAME}/{os.path.basename(backup_file)}"
    s3_client.upload_file(backup_file, S3_BUCKET_NAME, s3_object_key)
    logging.info("Backup uploaded to S3 successfully!")
except Exception as e:
    logging.error("An error occurred while uploading the backup to S3:")
    logging.error(str(e))

# Remove the compressed backup file
os.remove(backup_file)
""")

        # Check if the required command-line arguments are provided
        if len(sys.argv) < 9:
            print(
                "Usage: python mongo-to-s3.py -dHost <db_host> -dPort <db_port> -dName <db_name> -sName <s3_bucket_name> -sFolder <s3_folder_name> -sRegion <s3_region> [-cSchedule <cron_schedule>]")
            sys.exit(1)

        # Parse the command-line arguments
        args = sys.argv[1:]
        db_host = args[args.index("-dHost") + 1]
        db_port = int(args[args.index("-dPort") + 1])
        db_name = args[args.index("-dName") + 1]
        s3_bucket_name = args[args.index("-sName") + 1]
        s3_folder_name = args[args.index("-sFolder") + 1]
        s3_region = args[args.index("-sRegion") + 1]

        # Get user inputs
        db_user = input("Enter database username: ")
        db_pass = input("Enter database password: ")
        s3_access_key = input("Enter S3 access key: ")
        s3_secret_key = input("Enter S3 secret key: ")

        # Get the cron schedule from the command-line arguments
        cron_schedule = "0 */12 * * *"
        if "-cSchedule" in args:
            cron_index = args.index("-cSchedule") + 1
            if cron_index < len(args):
                cron_schedule = args[cron_index]

        # Substitute the placeholders in the template
        script_content = template.substitute(
            log_file=os.path.expanduser(
                f"~/mongo-to-s3-logs/{db_name}_log_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"),
            backup_dir=BACKUP_DIR,
            db_host=db_host,
            db_port=db_port,
            db_name=db_name,
            db_user=db_user,
            db_pass=db_pass,
            s3_bucket_name=s3_bucket_name,
            s3_folder_name=s3_folder_name,
            s3_access_key=s3_access_key,
            s3_secret_key=s3_secret_key,
            s3_region=s3_region
        )

        # Create the scripts directory if it doesn't exist
        scripts_dir = os.path.expanduser("~/mongo-to-s3-scripts")
        os.makedirs(scripts_dir, exist_ok=True)

        # Generate the script file name
        script_name = f"{db_name}-to-s3.py"

        # Save the generated script to the scripts directory
        script_path = os.path.join(scripts_dir, script_name)
        with open(script_path, "w") as f:
            f.write(script_content)

        # Set execute permission for the script
        os.chmod(script_path, 0o755)

        # Move the script to the user's home directory
        user_home_dir = os.path.expanduser("~")
        new_script_path = os.path.join(
            user_home_dir, "mongo-to-s3-scripts", script_name)
        os.makedirs(os.path.dirname(new_script_path), exist_ok=True)
        shutil.move(script_path, new_script_path)

        # Set the cronjob
        cron_command = f"{python_executable} {new_script_path}"
        cron_command_line = f"(crontab -l ; echo '{cron_schedule} {cron_command}') | crontab -"
        subprocess.run(cron_command_line, shell=True)

        print(
            f"Script '{script_name}' generated and placed in '{new_script_path}'.")
        print(
            f"Cronjob scheduled to run with the following schedule: {cron_schedule}")

    except KeyboardInterrupt:
        print("\nUser interrupted the program.")
        # Perform any necessary cleanup or exit gracefully
        sys.exit(0)


if __name__ == '__main__':
    main()
