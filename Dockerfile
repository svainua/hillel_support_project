FROM python:3.11.6-slim


#ENV PYTHONUNBUFFERED = 1   #показывает логи в консоли

# Update the system and install packages

RUN apt-get update -y \           
    && pip install --upgrade pip \    
    # dependencies to build Python packages
    && pip install --upgrade setuptools \
    && apt-get install -y build-essential \
    # install dependencies manager  
    && pip install pipenv watchdog \
    # cleaning up unused files
    && rm -rf /var/lib/apt/lists/*


# Install project dependencies
COPY ./Pipfile ./Pipfile.lock /

# setting dev dependencies and install it directly into the system (does not create virtual environment). Installing it globally
#RUN pipenv sync --dev --system

# убрали dev зависимости пир докеризации
RUN pipenv sync --system  

#TODO investigate
RUN pip install psycopg[binary]

# cd /app (get or create)
WORKDIR /app
COPY ./ ./  

EXPOSE 8000

ENTRYPOINT [ "python" ]
#CMD ["src/manage.py", "runserver"]

CMD ["src/manage.py", "runserver", "0.0.0.0:8000"]

