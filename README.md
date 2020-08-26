# Hitmen API

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/7cf534677c6e60d20370#?env%5BHitmen%5D=W3sia2V5Ijoic2Vzc2lvbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZX0seyJrZXkiOiJ1c2VyX2lkIiwidmFsdWUiOiI1ZjQ0NzNhOTI0NjIxMTBiM2Y1NTM3N2IiLCJlbmFibGVkIjp0cnVlfSx7ImtleSI6Im1hbmFnZXJfaWQiLCJ2YWx1ZSI6IjVmNDQ3MzZmMjQ2MjExMGIzZjU1Mzc3NyIsImVuYWJsZWQiOnRydWV9LHsia2V5IjoiZW1haWwiLCJ2YWx1ZSI6InZlZGFAZ21haWwuY29tIiwiZW5hYmxlZCI6dHJ1ZX0seyJrZXkiOiJwYXNzd29yZCIsInZhbHVlIjoiMTIzNDU2NzgiLCJlbmFibGVkIjp0cnVlfSx7ImtleSI6ImhpdF9pZCIsInZhbHVlIjoiNWY0NTZjN2IxNjE1YTRmOTdmYTQ1NDljIiwiZW5hYmxlZCI6dHJ1ZX1d)

## Requirements

* Docker
* Python 3
* virtualenv
* NodeJS
* Serverless CLI
* make command

## Installing requirements

### Docker

Make sure that you have docker and docker-compose available on your machine, if not,
you can install it on Ubuntu with the next command:

```shell script
sudo apt install docker docker-compose -y && sudo usermod -aG docker $USER
```

Now you need to start your machine to be able to use docker without `sudo`.

### Python3

Make sure that you have commands `python3` and `pip3` available on your shell, if not,
you can install it on Ubuntu with the next command:

```shell script
sudo apt install python3 python3-pip -y
``` 

### virtualenv

Virtualenv is used to keep all project dependencies agnostic to your local installation
by running an isolated and empty python environment, to use it you need to install it
on Ubuntu like this:

```shell script
sudo apt install python3-virtualenv -y
```

### NodeJS

NodeJS is used to install all Serverless framework dependencies and run the local server.
To install Node on your machine you can run the next command on Ubuntu:

```shell script
sudo apt install nodejs npm -y
```

### Serverless CLI

This is the main cli to use the framework of the project, to install it you can run the next 
command:

```shell script
npm install -g serverless
```

After this you should be able to execute `sls` and `serverless` commands on your shell.

### Make command

Make is used to write simple task related to the project like format, lint and run locally.
To install make you can run the next command:

```shell script
sudo apt install make -y
```

## Preparing environment

Once you have all requirements installed you need to prepare the project virtualenv, to do this 
follow the next commands:

```shell script
# Create a new virtualenv of python3.8
make venv

# Activate virtualenv
soruce venv/bin/activate

# Install project dependencies
make install
```

This will install all python and serverless dependencies of the project.
If you want to start using local python installation instead of project virtualenv, just run the 
`deactivate` command.

## First time running

The first time that the application will run you need to load the base users to use the API.
to do this, you need to run the next commands:

```shell script
# start local MongoDB instance
docker-compose up -d

# Load base users
python3 user_base.py
```

This will create all base users and assign managers to some Hitmen fto be able to work with data.
All data is persisted in `data/mongo/data` folder of the project.

## Running the API

To start the API you need to run the next command:
   
```shell script
make run
```

Before running this command you need to make sure that mongo docker instance is currently running.

## Extra make commands

* *Format code:* `make fmt` (requires black package)
* *Lint code:* `make lint` (requires pylint package)
* *Check Code Complexity:* `make complexity` (requires radon package)
* *Run tests:* `make test` (test files should be placed on tests folder) 

## Base Users

```json
[
    // Super User
    {
        "name": "Veda",
        "email": "veda@test.com",
        "password": "12345678",
        "description": "Celestial Being Founder"
    },
    // Managers
    {
        "name": "Sumeragui Le Noriega",
        "email": "sumeragui@test.com",
        "password": "12345678",
        "description": "Gundam Manager"
    },
    {
        "name": "Christina Sierra",
        "email": "christina@test.com",
        "password": "12345678",
        "description": "Gundam Manager"
    },
    {
        "name": "Feldt Grace",
        "email": "feldt@test.com",
        "password": "12345678",
        "description": "Gundam Manager"
    },
    // Hitmen
    {
        "name": "Setsuna F. Seiei",
        "email": "setsuna@test.com",
        "password": "12345678",
        "description": "Gundam Master"
    },
    {
        "name": "Tieria Erde",
        "email": "tieria@test.com",
        "password": "12345678",
        "description": "Gundam Master"
    },
    {
        "name": "Lockon Stratos",
        "email": "lockon@test.com",
        "password": "12345678",
        "description": "Gundam Master"
    },
    {
        "name": "Allelujah Haptism",
        "email": "allelujah@test.com",
        "password": "12345678",
        "description": "Gundam Master"
    },
    {
        "name": "Nena Trinity",
        "email": "nena@test.com",
        "password": "12345678",
        "description": "Gundam Master"
    }
]
```