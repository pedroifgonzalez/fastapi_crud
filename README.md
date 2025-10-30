# FastAPI CRUD

## Welcome to a simple but curated FastAPI CRUD example app

### Table of Contents

Project structure

## Project Structure

The app structure was designed to keep it simple, however organized.

- The expected configuration to run the app properly is expected to be
in the `core` folder, which also expects any security and middleware layers.
- The `models` folder contains all the model definitions the app uses.
- Within the `routers` folders live all the router modules per domain.
- The `schemas` folder will handle the input and output data, including
their validations.
- All code-related business logic must be in the `services` folder.
- There's still space for helper functions, generic pagination, and custom
validations in the `utils` folder.
