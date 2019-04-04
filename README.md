# Coati Test

* Hacer un webservice usando Python o Node que tenga una sola entidad llamada Usuarios.
* Los usuarios deben contar con un identificador principal, un rol y un password que no se encuentre en texto plano.
* Deberá haber un método en el que los usuarios puedan hacer login.
* Los usuarios deben poder ver la lista de los demas usuarios solo cuando se encuentren logueados.
* La aplicación no debe de usar sesiones.
* La aplicación implementá JWT
* Los roles contemplados son admin y user, solo los usuarios con rol admin, pueden crear, editar o borrar usuarios.

## Requerimentos

* Python 2.7
* Django 1.11
* Django Rest Framework

### Instalación

Descargar repositorio:

```
https://github.com/greciamb/coati_test
```

### Descargar requerimentos

Correr en consola:

```
pip install -r requirements.txt
```

## DB

Correr en consola:

```
python manage.py makemigrations

python manage.py migrate
```

Crear super usuario:

```
python manage.py createsuperuser
```

### Montar servidor
Correr django:

```
python manage.py runserver
```

El proyecto se correrá en la dirección:

```
localhost:8000
```

### Creando el primer usuari con role admin.

Diríjase a la siguiente dirección:

```
http://localhost:8000/admin
```

utilice el usuario y contraseña definidos cuando se creó el super usuario anteriormente. Entrar a la tabla nombrada "Usuarioss" y cree un usuario tipo '1', asigne usuario y contraseña.


## Pruebas en Postman

En la siguiente liga podrá encontrar los endpoints sobre los cuáles podrá hacer pruebas:

```
https://documenter.getpostman.com/view/2807737/S1EH4Mrt
```
