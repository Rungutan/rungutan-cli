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
    rungutan domains --help
    rungutan team --help
    rungutan results --help
    rungutan raw_results --help
    rungutan tests --help
    rungutan templates --help
    rungutan crons --help
    rungutan notifications --help
    rungutan vault --help

Rungutan CLI utility for interacting with https://rungutan.com

positional arguments:
  command     Command to run

optional arguments:
  -h, --help  show this help message and exit


```

* Check the help menu for a specific command

```shell script
$ rungutan domains --help
usage: rungutan [-h] [--domain_name DOMAIN_NAME] [-p PROFILE]
                [{list,validate,remove,add}]

Domain command system

positional arguments:
  {list,validate,remove,add}

optional arguments:
  -h, --help            show this help message and exit
  --domain_name DOMAIN_NAME
                        Required parameter for subcommand ["validate", "remove", "add"]
  -p PROFILE, --profile PROFILE
                        The profile you'll be using.
                        If not specified, the "default" profile will be used. 
                        If no profiles are defined, the following env variables will be checked:
                        * RUNGUTAN_TEAM_ID
                        * RUNGUTAN_API_KEY
```

* Actually run a command

```shell script
$ rungutan domains list
{
    "Domains": [
        {
            "domain_name": "rungutan.com",
            "domain_state": "validated",
            "validation_method": "DNS",
            "submitted_date": "2020-01-22T09:43:08Z",
            "validated_date": "2020-01-22T09:46:19Z",
            "validation_code": "AQICAHhHp5r6gwXOjYqwtC9i+eAkDkjIWY6fFcvReCnBELkoNQE9gtS6zGZytyLbOH36UN9nAAAAZjBkBgkqhkiG9w0BBwagVzBVAgEAMFAGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMEaZoxNmA88dZOjH1AgEQgCPHSkRXDs7qGl6lpEqoqA/K0deoSpuhveJihfstbYgTz6nQRg=="
        }
    ]
}
```

## Run it as a docker container

* Using local volume

```shell script
$ docker run \
  -v ${HOME}/.runtugan:/root/.rungutan \
  rungutancommunity/rungutan-cli:latest "rungutan tests --help"
usage: rungutan [-h] [--test_id TEST_ID] [--test_file TEST_FILE]
                [--test_public {public,private}] [--test_name TEST_NAME]
                [--wait_to_finish] [-p PROFILE]
                [{list,add,cancel,remove,get,preview-credits,set-sharing}]

Tests command system

positional arguments:
  {list,add,cancel,remove,get,preview-credits,set-sharing}

optional arguments:
  -h, --help            show this help message and exit
  --test_id TEST_ID     Required parameter for subcommand ["cancel", "get", "set-sharing", "remove"].
                        Optional parameter for subcommand ["list"]
  --test_file TEST_FILE
                        Required parameter for subcommand ["add", "preview-credits"]. 
                        You can specify --test_file or --template_id, but not both!
  --template_id TEMPLATE_ID
                        Required parameter for subcommand ["add", "preview-credits"]. 
                        You can specify --test_file or --template_id, but not both!
  --test_public {public,private}
                        Required parameter for subcommand ["set-sharing"]
  --test_name TEST_NAME
                        Optional parameter for subcommand ["add", "preview-credits"].
                        Use it to override the value for "test_name" in your test_file or to simply specify a name for the test
  --wait_to_finish      Optional parameter for subcommand ["add"]
                        Use it to set the CLI to wait for the test to finish before exiting.
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
  rungutancommunity/rungutan-cli:latest "rungutan domains --help"
usage: rungutan [-h] [--domain_name DOMAIN_NAME] [-p PROFILE]
                [{list,validate,remove,add}]

Domain command system

positional arguments:
  {list,validate,remove,add}

optional arguments:
  -h, --help            show this help message and exit
  --domain_name DOMAIN_NAME
                        Required parameter for subcommand ["validate", "remove", "add"]
  -p PROFILE, --profile PROFILE
                        The profile you'll be using.
                        If not specified, the "default" profile will be used. 
                        If no profiles are defined, the following env variables will be checked:
                        * RUNGUTAN_TEAM_ID
                        * RUNGUTAN_API_KEY

```
