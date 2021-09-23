# [facetagram](myfacetagram.herokuapp.com)
Facetagram is my personal project where you can make new friends, share your photos and communicate with them.  
## Feautures
* Authenticate
* Send and accept friend requests
* Share Posts
* Like and dislike posts
* Write Comments to posts
* Like and dislike comments
* Chat

## Languages, frameworks and libraries
### Frontend
* [Html](https://developer.mozilla.org/en-US/docs/Web/HTML)
* [Css](https://developer.mozilla.org/en-US/docs/Web/CSS)
* [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
* [Bootstrap 5](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
* [Font Awesome](https://fontawesome.com/)
* [JQuery](https://jquery.com/)
* [InfiniteJs](https://airbnb.io/infinity/)
* [Waypoints](http://imakewebthings.com/waypoints/)
### Backend
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [PostgreSQL](https://www.postgresql.org/)
### Deployment
* Deployed on [Heroku](https://www.heroku.com/)
* Static files storage [**Whitenoise**](http://whitenoise.evans.io/)
* Media files storage [**Cloudinary**](https://cloudinary.com/)
## **Setup**

__Make sure that you have python3 setup that can be referenced with command python to easily follow the tutorial. If your python is refernced with python3, then replace all pythons with python3__

## Install Docker
### For Linux
```
$ sudo apt-get install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg-agent \
  software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository \
                "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
                $(lsb_release -cs) \
                stable"
$ sudo apt-get update
$ sudo apt-get install -y docker-ce docker-ce-cli containerd.io
$ sudo usermod -aG docker "$USER"
```

### For Windows

Follow the steps [here](https://docs.docker.com/docker-for-windows/install/)

## Download postgres image and run it with Docker

### For Linux

```
$ sudo apt-get update
$ sudo apt-get install python-pip python-dev libpq-dev
$ pip install --upgrade pip
$ sudo docker run -d --name postgres --restart always -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres postgres -e POSTGRES_DB=facetagram
```

### For Windows
```
$ python -m pip install --upgrade pip
$ docker run -d --name postgres --restart always -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres postgres -e POSTGRES_DB=facetagram
```

__Your terminal must be in the root of the facetagram project for all the commands below !!__

## Create Python virtual environment
### For Linux
```
$ sudo pip install virtualenv
$ mkdir ~/myproject
$ cd ~/myproject
$ virtualenv venv
$ source venv/bin/activate
```
_If you have any issues with the virtual environment installation on Linux please check [this](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b)_

### For Windows
```
$ python -m pip install --user virtualenv
$ mkdir /makalam_env
$ cd /makalam_env
$ python -m venv /makalam_env
$ /makalam_env/Scripts/activate
```
_If you have any issues with the virtual environment installation on Windows please check [this](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)_

## Install dependencies, migrate db, create superuser and run the server
### For Linux and Windows
```
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```