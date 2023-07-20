# Migrator

Aiming to create a sidecar to create databases for services. **It only meant for local development**

## Usage
The way to use this repo is to clone or fork it for your local development.
you can check all commands in `Makefile`, but here is highlights:

- Create a new database with same User and password as database name; 
assuming your database name is the same as your service name

    ```shell
    make create service={serviceName}
    ```

- Migrate the changes

    ```shell
    make migrate
    ```

- to add more python packages

    ```shell
    make add package={package_name}
    ```


TODO:
- add the commands of create and migrate as container commands
- push dockerhub image with README file.