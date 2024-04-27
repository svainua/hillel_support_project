FROM --platform=linux/arm64/v8 python:3.11.6-slim

# Update the system and install packages

RUN apt-get update -y \           
    && pip install --upgrade pip \    
    # dependencies to build Python packages
    && pip install --upgrade setuptools \
    && apt-get install -y build-essential \
    # install dependencies manager  
    && pip install pipenv \
    # cleaning up unused files
    && rm -rf /var/lib/apt/lists/*


# Install project dependencies
COPY ./Pipfile ./Pipfile.lock /

# setting dev dependencies and install it directly into the system (does not create virtual environment). Installing it globally
RUN pipenv sync --dev --system

#TODO investigate
RUN pip install psycopg[binary]


# cd /app (get or create)
WORKDIR /app
COPY ./ ./  


EXPOSE 8000

ENTRYPOINT [ "python" ]
CMD ["src/manage.py", "runserver"]



