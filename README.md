# Django-Url-Shortener
url-shortener is a django app that shortens the urls that it receives using pyshorteners module in python


## Stacks
* The project is written in Django .

* Authentication is really simple using user_name and password given from users .

* Postgresql is the main database for the project .
* Gunicorn is used for production side to act as WSGI HTTP Server .
* Nginx is also used for production side to act as a webserver for static files and a reverse proxy for the django .

** The project is also Dockerized, meaning that all the components mentioned are communicating with each other through networking. all the docker files are inside the project repo.



 
## Stack Badges

[![](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

[![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://www.djangoproject.com/)

[![](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://www.nginx.com/)

[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/)

	
## Installation

Clone the project from the git lab repo

```bash
  git clone {repo-gitlab-url}
```
#### There are 2 ways to run the project locally
### Option 1 (without Docker):
To install PostgreSQL, first refresh your server’s local package index:

```bash
sudo apt update
```

Install postgresql (version 12 or above)
```bash
sudo apt install postgresql postgresql-contrib
```

Access postgres prompt via postgres default user and default database
by using **psql** command
```bash
psql -U postgres -d postgres
```

Create a database to use (name it according to DATABASE_NAME in sample.env)
```bash
create database {DATABASE_NAME};
```

Create your database user (name it according to DATABASE_USER_NAME and DATABASE_USER_PASSWORD in sample.env)
```bash
create user {DATABSE_USER_NAME} with encrypted password '{DATABASE_USER_PASSWORD}';
```


Create a virtual environment using **venv** module in python. Create it inside ur_shortener_app directory

```
python3 -m venv env

```

Activate the environment.
```
source env/bin/activate

```

Install all python libraries needed for project from requirements.txt file inside url_shortener_app directory using **pip** module.

```
pip install -r {path-to-requirements.txt file}

```

After all the modules have been installed, make a copy from sample.env file inside url_shortener_app directory and rename it to .env (this file has all the data needed to run the project):

```
cp sample.env .env

```

Run the project using **runserver** command

```
python manage.py runserver

```
### Option 2 (with Docker):
make a copy from sample.env file inside url_shortener_app directory and rename it to .env (this file has all the data needed to run the project):

```
cp sample.env .env

```
To install Docker and docker compose on Ubuntu, issue the following commands in a terminal window:
<pre><code>
### Docker and docker compose prerequisites
sudo apt-get install curl
sudo apt-get install gnupg
sudo apt-get install ca-certificates
sudo apt-get install lsb-release
### Download the docker gpg file to Ubuntu
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

### Add Docker and docker compose support to the Ubuntu's packages list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-pluginsudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-pluginlinux/ubuntu   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
</code></pre>

Add the docker group if it doesn't already exist:

```
 sudo groupadd docker
```

Add the connected user "$USER" to the docker group. Change the user name to match your preferred user if you do not want to use your current user:

```
 sudo gpasswd -a $USER docker
 # Either do a newgrp docker or log out/in to activate the changes to groups.
```

for local side a file is used called docker-compose.yml

docker-compose.yml:
<pre><code>
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    expose:
      - 8000
    networks:
      - django-network
    depends_on:
      - db
    command: ["./wait-for-it.sh"]
    volumes:
      - static_volume:/code/staticfiles
  db:
    image: postgres
    volumes:
      - postgresdb:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=test_url_shortener
      - POSTGRES_USER=user1
      - POSTGRES_PASSWORD=123
    ports:
      - 5432:5432
    networks:
      - django-network
networks:
  django-network:
    name: django-network
volumes:
  postgresdb:
  static_volume:

</code></pre>

wait-for-it.sh is a shell script that checks if the postgresql container is up via nc tool, and then runs the migrations and  starts the server 

wait-for-it-dev.sh:
<pre><code>
#!/bin/bash
until nc -z -v -w30 db 5432
do
    echo db
    echo 5455
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done
python3 manage.py migrate
python3 manage.py runserver 8000
</code></pre>

simply run this command inside the url_shortener_app directory to create the needed Docker images and create and run the containers

```
docker-compose up -d --build 
```

### Production (with Docker):
#### if you want to dockerize and deploy on a web server
install docker and docker-compose just like option 2

Create a directory alongside the url_shortener_app directory called nginx with two files: Dockerfile and default.conf (the directory name can be anything).

The contents of these two files are as follows:
<pre><code>
#Dockerfile
FROM nginx:stable-alpine
COPY default.conf /etc/nginx
COPY default.conf /etc/nginx/conf.d
EXPOSE 80

#nginx.conf
server {
    listen 80 default_server;
    server_name _;
    location / {
        proxy_pass http://web:8000;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
    location /static/ {
        alias /app/static/;
    }
    location /media/ {
        alias /app/static/;
    }
}
</code></pre>

for production side another file is used called docker-compose.dev.yml
docker-compose.dev.yml:
<pre><code>
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    expose:
      - 8000
    networks:
      - django-network
    depends_on:
      - db
    command: ["./wait-for-it-dev.sh"]
    volumes:
      - static_volume:/code/staticfiles
  db:
    image: postgres
    volumes:
      - postgresdb:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=test_url_shortener
      - POSTGRES_USER=user1
      - POSTGRES_PASSWORD=123
    ports:
      - 5432:5432
    networks:
      - django-network
  nginx:
    build: ../nginx
    volumes:
      - static_volume:/code/staticfiles
    ports:
      - 80:80
    depends_on:
      - web
    networks:
      - django-network
networks:
  django-network:
    name: django-network
volumes:
  postgresdb:
  static_volume:
</code></pre>

wait-for-it-dev.sh is a shell script that checks if the postgresql container is up via nc tool, and then runs the migrations, collects static files for nginx to serve and  starts the server with gunicorn

wait-for-it-dev.sh:
<pre><code>
#!/bin/bash
until nc -z -v -w30 db 5432
do
    echo db
    echo 5455
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done
python3 manage.py migrate
python3 manage.py collectstatic
gunicorn url_shortener_app.wsgi:application --bind 0.0.0.0:8000 --workers=4
</code></pre>

simply run this command inside the url_shortener_app directory to create the needed Docker images and create and run the containers

```
docker-compose -f docker-compose.dev.yml up -d --build
```


# Django Apps that are created in the project
## Core App
#### This is the main app that handles authentication and also provides the url shortening API

### models.py
#### This file contains the only model used in the project called User. it inherits from the **AbstractBaseUser** and **PermissionsMixin** classes inorder to create a custom User model for the project.
#### There is a manager class for the User class called **UserManager**, it is the interface through which database query operations are provided to User model
User model class:
<pre><code>
class User(AbstractBaseUser, PermissionsMixin):
    # Configs
    USERNAME_FIELD = 'mobile_number'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Model fields
    mobile_number = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.get_username()

    @classmethod
    def get_by_id(cls, user_id):
        try:
            user = cls.objects.get(pk=user_id)
            return user
        except cls.DoesNotExist:
            raise ObjectDoesNotExist

</code></pre>

UserManager class:
<pre><code>
class UserManager(BaseUserManager):
    def create_user(self, mobile_number, email, is_active, password=None):
        """
        Creates and saves a User with the given email, mobile_number, is_active and password.
        """
        if not mobile_number:
            raise ValueError('Users must have a mobile number')
        if len(mobile_number) != 11 or mobile_number[0:2] != '09':
            raise ValueError('Invalid mobile number')
        user = self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            is_active=is_active,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
</code></pre>

### forms.py
#### This file contains the necessary forms that are used for django Generic Views in views.py, they describe a form and determine how it works and appears. the validation for each declared field is being done via the clean_{field name} function, or in some cases via clean function(for all fields at once)
####  RegisterForm is used to get registration data from the user and create a user in the database if the data that was sent is valid
RegisterForm class:
<pre><code>
class RegisterForm(forms.ModelForm):
    mobile_number = forms.CharField(max_length=50, required=True,
                                    widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    email = forms.CharField(max_length=50, required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=128, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(max_length=128, required=True,
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))

    class Meta:
        model = User
        fields = ['email', 'mobile_number', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        email = cleaned_data.get('email')
        mobile_number = cleaned_data.get('mobile_number')
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        validate = EmailValidator()
        try:
            validate(email)
        except ValidationError as e:
            self.add_error('email', 'Entered email address is not valid.')
        try:
            if not re.match(r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$',
                            mobile_number):
                raise
        except:
            self.add_error('mobile_number', 'Please write a valid mobile number.')
        if password != confirm_password:
            self.add_error('password', "password and confirmation password do not match")

    def save(self):
        user = User.objects.create_user(
            mobile_number=self.instance.mobile_number,
            email=self.instance.email,
            is_active=True,
            password=self.instance.password
        )
        return user

</code></pre>

####  LoginForm is used to get login data from the user and authenticate the user if the data that was sent is valid
LoginForm class:
<pre><code>
class LoginForm(forms.ModelForm):
    mobile_number = forms.CharField(max_length=50, required=True,
                                    widget=forms.TextInput(attrs={'placeholder': 'Mobile Number'}))
    password = forms.CharField(max_length=128, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['mobile_number', 'password']

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        try:
            if not re.match(r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$',
                            mobile_number):
                raise
        except:
            raise ValidationError('Please write a valid mobile number.', code='invalid')
        exists = User.objects.filter(mobile_number=mobile_number).first()
        if not exists:
            raise ValidationError('User with this mobile number does not exist.', code='invalid')
        return mobile_number

    def clean_password(self):
        password = self.cleaned_data['password']
        mobile_number = self.cleaned_data.get('mobile_number', None)
        if not mobile_number:
            return password
        user = User.objects.get(mobile_number=self.cleaned_data['mobile_number'])
        if not user.check_password(password):
            raise ValidationError('Password is incorrect.', code='invalid')
        return password

    def clean(self):
        # we override the clean method to change the _validate_unique attribute to bypass validate_unique for mobile_number
        self._validate_unique = False
        return self.cleaned_data

</code></pre>

####  ShortenUrlForm is used to get the desired URL from user and return it to the view to get shortened after being validated.
ShortenUrlForm class:
<pre><code>
class ShortenUrlForm(forms.Form):
    url = forms.CharField(max_length=2048, required=True,
                          widget=forms.TextInput(attrs={'placeholder': 'URL'}),
                          validators=[URLValidator, ])

    def clean_url(self):
        url = self.cleaned_data['url']
        validate = URLValidator()
        try:
            validate(url)
        except ValidationError as e:
            raise ValidationError('Entered URL is not Valid!', code='invalid')
        return url
</code></pre>


- **set_available** [This function removes agent's id from all the area lists that agent was in them with set_unavailable function and sets the new area id in the proper area list based on agent's status, it works directly with redis]
- **set_unavailable** [This function removes agent's id from the area lists that agent was in them and sets agent's status to offline, it works directly with redis]
- **change_area** [This function removes agent's id from previous area's list in redis and adds agent's id to the new area's list in redis, it works directly with redis]

### views.py
#### This file contains the necessary view functions and GenericView classes that are used to respond to each url.
####  redirect_home function is used to redirect user to the homepage, it uses reverse shortcut to call the home url.
redirect_home function:
<pre><code>
def redirect_home(request):
    return HttpResponseRedirect(reverse('core:home'))
</code></pre>

####  home function is used to load homepage html file with the given parameters', it uses the render shortcut to load a template with the option to send context data
home function:
<pre><code>
def home(request, **kwargs):
    user_login_required = kwargs.get('login_required', False)
    return render(request, 'home.html', context={'login_required': user_login_required})
</code></pre>

####  login_required function is used as a workaround to handle the redirection of users that are not logged in which is being called by the LoginRequiredMixin Class that is used as a parent for ShortenUrlView generic View. it just calls the home function with extra kwarg
login_required function:
<pre><code>
def login_required(request):
    return home(request, login_required=True)
</code></pre>

####  logout_view function is used to log out and redirect the user to the home page.
logout_view function:
<pre><code>
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:home'))
</code></pre>
####  RegisterView class is used to get registration data from the user and create the user if the data that was sent is valid, if the data is invalid, it will render home template  with form errors
RegisterView class:
<pre><code>
class RegisterView(FormView):
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('core:home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return redirect('core:home')

    def form_invalid(self, form):
        return render(self.request, 'home.html', {'register_form': form})

</code></pre>

####  LoginView class is used to get login data from the user and authenticate the user if the data that was sent is valid, if the data is invalid, it will render home template  with form errors
RegisterView class:
<pre><code>
class LoginView(FormView):
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('core:home')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['mobile_number'],
            password=form.cleaned_data['password'],
        )
        if user is not None:
            login(self.request, user)
            return redirect('core:home')

    def form_invalid(self, form):
        return render(self.request, 'home.html', {'login_form': form})
</code></pre>

####  ShortenUrlView class is used to get the desired url from the user and shorten it using pyshortener object, it inherits from **LoginRequiredMixin** class which guarantees that the users should be logged in inorder to use the View class, it will render home template with errors if the entered url is not valid
ShortenUrlView class:
<pre><code>
class ShortenUrlView(LoginRequiredMixin, FormView):
    form_class = ShortenUrlForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('core:home')

    def form_valid(self, form):
        url = form.cleaned_data['url']
        shortener = pyshorteners.Shortener()
        shortened_url = shortener.osdb.short(url)
        context = {'shortened_url': shortened_url,
                   'url': url}
        return render(self.request, 'home.html', context=context)

    def form_invalid(self, form):
        return render(self.request, 'home.html', {'url_form': form})
</code></pre>

