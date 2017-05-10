# Gestor de salones de reuniones

## Instalación

* Clonar proyecto

    `git clone https://github.com/lfbos/meeting_room_management.git`

* Acceder al proyecto

    `cd meeting_room_management`

* Crear python environment

    * Virtualenvwrapper: utilizando [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/):

        ```
        mkvirtualenv env_name --python=python2 # si se tiene python por defecto con python3
        pip install -r requirements.txt
        ```

    * Virtualenv: utilizando [virtualenv](https://virtualenv.pypa.io/en/stable/):

        ```
        virtualenv env
        source env/bin/activate
        pip install -r requirements.txt
        ```

* Crear base de datos en postgres

* Crear archivo `.env` y añadir la información de postgres (ver .env.example)

* Migrar a la base de datos `python manage.py migrate`

* Crear super usuario `python manage.py createsuperuser`

* Ejecutar e ir a [http://localhost:8000/admin](http://localhost:8000/admin)

# Uso

Es necesario ingresar primero a el admin de django (con el usuario creado en la parte de instalación) y crear los modelos necesarios para interactuar, en teoría solo se necesita crear un usuario del portal con el rol de Administrador, después de eso se puede ir a [http://localhost:8000/](http://localhost:8000/)
