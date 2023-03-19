# Coffee Shop Full Stack

## Full Stack Nano - IAM Final Project

`CRUD` - app:       
Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard.

Full stack drink menu application. The application scope of functionality:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

## Authors
Jany Muong           
Udacity

## Tasks

Start by reading the READMEs in:

1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

## Tech Stack

Developers should have `node and npm`, `ionic cli`, `python3 and pip`.       
This is a full-stack application designed with some key functional areas listed out below:

### Backend

The `./backend` directory contains a Flask server, with a SQLAlchemy module to simplify your data needs. This is a complete API with the required endpoints, configuration, and integrates smoothly with `Auth0` for **authentication** and **authorization**.

[View the README.md within ./backend/ for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. You might want to only need to update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app.

[View the README.md within ./frontend/ for more details.](./frontend/README.md)
