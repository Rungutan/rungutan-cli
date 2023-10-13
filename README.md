# rungutan-cli

## What is Rungutan?

[Rungutan](https://rungutan.com) is the first API Load Testing SaaS platform worldwide, 100% Serverless, which  helps you simulate workflows to emulate user experience, so it's easier to design workflow oriented strategies.


## Where do I sign up?

Although we love our [landing page](https://rungutan.com) and we definitely think it's worth checking out, you can sign up directly by going on [https://app.rungutan.com/signup](https://app.rungutan.com/signup)

## Do you have any ACTUAL documentation?

D'oh.

You can find it on our [Docs](https://docs.rungutan.com) page. 


## Why use the CLI?

This CLI has been designed for:
1) perform load testing directly within a CI/CD process
2) run any command that you would do on the web platform directly in your terminal

## How to install the CLI?

```shell script
pip install rungutan
```

## How to run the CLI?

* Set up your authentication mechanism using the Rungutan API key

```shell script
rungutan configure (--profile some-profile-name)
```

* Check the overall help menu

```shell script
$ rungutan help

usage: rungutan <command> [<args>]

To see help text, you can run:
    rungutan help
    rungutan version
    rungutan configure --help
    rungutan team --help
    rungutan results --help
    rungutan raw_results --help
    rungutan tests --help
    rungutan templates --help
    rungutan crons --help
    rungutan notifications --help
    rungutan vault --help
    rungutan csv --help
    rungutan file --help

Rungutan CLI utility for interacting with https://rungutan.com

positional arguments:
  command     Command to run

optional arguments:
  -h, --help  show this help message and exit


```

* Check the help menu for a specific command

```shell script
$  rungutan csv --help
usage: rungutan [-h] [--csv_id CSV_ID] [-p PROFILE] [{list,get,remove}]

CSV command system

positional arguments:
  {list,get,remove}

optional arguments:
  -h, --help            show this help message and exit
  --csv_id CSV_ID       Required parameter for subcommand ["get", "remove"].
                        Optional parameter for subcommand ["list"].
  -p PROFILE, --profile PROFILE
                        The profile you'll be using.
                        If not specified, the "default" profile will be used.
                        If no profiles are defined, the following env variables will be checked:
                        * RUNGUTAN_TEAM_ID
                        * RUNGUTAN_API_KEY
```

* Actually run a command

```shell script
$ rungutan csv list
{
    "CSV": [
        {
            "csv_id": "9c30cffe-ea4b-440e-aa73-9182ab98eb80",
            "file_name_csv": "sample",
            "member_email": "support@rungutan.com",
            "uploaded_date": "2021-10-05T11:25:11Z",
            "max_rows": "25",
            "max_columns": "7"
        }
    ]
}
```

## Run it as a docker container

* Using local volume

```shell script
$ docker run \
  -v ${HOME}/.rungutan:/root/.rungutan \
  rungutancommunity/rungutan-cli:latest rungutan csv --help
usage: rungutan [-h] [--csv_id CSV_ID] [-p PROFILE] [{list,get,remove}]

CSV command system

positional arguments:
  {list,get,remove}

optional arguments:
  -h, --help            show this help message and exit
  --csv_id CSV_ID       Required parameter for subcommand ["get", "remove"].
                        Optional parameter for subcommand ["list"].
  -p PROFILE, --profile PROFILE
                        The profile you'll be using.
                        If not specified, the "default" profile will be used.
                        If no profiles are defined, the following env variables will be checked:
                        * RUNGUTAN_TEAM_ID
                        * RUNGUTAN_API_KEY
```

* Or using environment variables

```shell script
$ docker run \
  -e RUNGUTAN_TEAM_ID=my_team \
  -e RUNGUTAN_API_KEY=my_api_key \
  rungutancommunity/rungutan-cli:latest rungutan csv --help
usage: rungutan [-h] [--csv_id CSV_ID] [-p PROFILE] [{list,get,remove}]

CSV command system

positional arguments:
  {list,get,remove}

optional arguments:
  -h, --help            show this help message and exit
  --csv_id CSV_ID       Required parameter for subcommand ["get", "remove"].
                        Optional parameter for subcommand ["list"].
  -p PROFILE, --profile PROFILE
                        The profile you'll be using.
                        If not specified, the "default" profile will be used.
                        If no profiles are defined, the following env variables will be checked:
                        * RUNGUTAN_TEAM_ID
                        * RUNGUTAN_API_KEY

```
