# mongo-to-s3

The `mongo-to-s3` package provides a convenient way to backup MongoDB databases and upload the backups to Amazon S3 for safekeeping. This utility allows you to automate the backup process and ensure the security and availability of your MongoDB data.

## Features

-   Automatically creates backups of MongoDB databases.
-   Compresses backups and stores them securely in Amazon S3.
-   Generates customizable backup scripts based on user inputs.
-   Supports scheduling backup jobs using cron.
-   Provides logging functionality to track backup activity and errors.

## Installation

1. Ensure you have Python 3 installed on your system.

2. Install the package using pip:

    ```shell
    pip install mongo-to-s3
    ```

## Usage

1. Open a terminal or command prompt.

2. Run the `mongo-to-s3` command with the required options,

    ```shell
    mongo-to-s3 -dHost <db_host> -dPort <db_port> -dName <db_name> -sName <s3_bucket_name> -sFolder <s3_folder_name> -sRegion <s3_region>
    ```

    Replace the placeholders (`<db_host>`, `<db_port>`, `<db_name>`, `<s3_bucket_name>`, `<s3_folder_name>`, `<s3_region>`) with the appropriate values for your setup.

3. You will be prompted to enter the database username, database password, S3 access key, and S3 secret key.

4. The backup script will be generated and scheduled to run using cronjobs. By default, it will run every 12 hours. You can customize the cron schedule by adding the `-cSchedule` option followed by the desired schedule.

    ```shell
    mongo-to-s3 -dHost <db_host> -dPort <db_port> -dName <db_name> -sName <s3_bucket_name> -sFolder <s3_folder_name> -sRegion <s3_region> -cSchedule "0 0 * * *"
    ```

    This example schedules the backup to run daily at midnight.

5. The generated backup script will be placed in the mongo-to-s3-scripts directory in the user's home directory.

    You can generate backup script for all of your MongoDB databases this way.

### Logs

The `mongo-to-s3` utility creates log files for each backup operation. The log files contain information about the backup process and any errors that may have occurred. By default, the log files are stored in the `mongo-to-s3-logs` directory in the user's home directory.

You can check the logs to monitor the backup activity and troubleshoot any issues that may arise. The log file names follow the format: `<db_name>_log_<timestamp>.txt`.

To view the logs, navigate to the `mongo-to-s3-logs` directory:

```shell
cd ~/mongo-to-s3-logs
```

## Contributing and Feedback

Contributions, bug reports, and feature requests are welcome! If you encounter any issues or have ideas to improve `mongo-to-s3`, please check the [Issue Tracker](https://github.com/IamLizu/mongo-to-s3/issues) for existing issues or open a new one.

If you would like to contribute code to the project, you can follow these steps:

1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine.
3. Make changes and test them thoroughly.
4. Commit your changes and push them to your forked repository.
5. Submit a pull request to the main repository.

Your contributions are highly appreciated, whether it's fixing a bug, adding a new feature, or improving documentation.

Additionally, I encourage you to provide feedback and suggestions for the project. You can open an issue to share your thoughts, ideas, or any questions you may have.

Let's make `mongo-to-s3` even better together!
