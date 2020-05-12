# rungutan-cli

## What is Rungutan?

[Rungutan](https://rungutan.com) is the first Load Testing Tool! 100% serverless, API driven & accessible for all tech professionals.

As an evolved creature, Rungutan has extensive Load-Testing abilities, gained by experience, in order to survive in a fast-paced environment. Load Testing is its first language, so you will get along very well.

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
    rungutan configure --help
    rungutan domain --help
    rungutan team --help
    rungutan results --help
    rungutan tests --help
    rungutan crons --help

Rungutan CLI utility for interacting with https://rungutan.com

positional arguments:
  command     Command to run

optional arguments:
  -h, --help  show this help message and exit

```

* Check the help menu for a specific command
```shell script
$ rungutan domain list --profile rungutan
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
