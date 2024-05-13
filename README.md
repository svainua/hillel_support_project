# About

This is an educational project for Hillel

# pipenv usage

Pipeng is used as a main package manager on the project. For more information please follof the [documentation](https://pipenv.pypa.io/en/latest/)

```sh

# creating a new virtual environment
pipenv shell

# creating a .lock file from Pipenv file
pipenv lock

# installing dependencies from .lock file
pipenv sync
```



# Deploy with Docker Compose

'''sh
copy .env.default from .env
docker compose build && docker compose up -d

'''

# Some useful commands

'''
# Look for 20 last logs lines and follow stdout until Ctrl-C
docker compose logs --tail 20 -f api

# Execute the command inside the container
docker compose exec api <command>
'''

