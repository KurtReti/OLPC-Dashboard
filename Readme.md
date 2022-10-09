Clone or download repository to desired location </br>
The project has been developed and tested using Python 3.9</br>
cd to base directory location and run in command line <i>pip install -r requirements.txt</i> </br>
The following environment variables must be set for the app to work properly: </br>
For database connection a complete connection string can be used with environment variable <i>DB_URI</i> which is a
complete connection string e.g. postgresql+psycopg2://scott:tiger@host/dbname</br>
The connection string variables can also be separately set using following environment variables: </br>
<i>DB_TYPE</i> - database type + python connector e.g. postgresql+psycopg2</br>
<i>DB_NAME</i> - database name </br>
<i>DB_HOST</i> - host of the database </br>
<i>DB_USER</i> - username </br>
<i>DB_PASS</i> - password </br>
<i>DB_PORT</i> - port</br>
For displaying graph maps the <i>MAPBOX_TOKEN</i> must be set <i>MAPBOX_TOKEN</i></br>
Other environment variables that can be set are REDIS_URL which allows for caching of functions to improve performance
and DEBUG which enables debugging mode in Dash </br>
then run <i>python index.py</i> from the base directory </br>
app will be running at address [http://127.0.0.1:8050](http://127.0.0.1:8050) by default</br>
The app is designed to be used with Heroku. Login to Heroku and create your app.</br>
To install on heroku, download the Heroku CLI</br>
Then run _heroku login_ in command line and following prompts to login While in the cloned repository run
_git remote add heroku https://git.heroku.com/app_name.git_ where app_name is the name you have given your created app
in heroku commit any changes to the repository run command _git push heroku branch:master_ where branch is the branch
you want to deploy There is also an option to use sqlite as database as Heroku free tier does not allow enough database
storage for the project requirements. To enable this set DB_TYPE = "sqlite" and DB_NAME as the desired filename of
database <br>
Then create a new branch from the master branch and edit the .gitignore and remove *.db line. </br>
Then from the data_import folder run python create_sampled_activity_data.py to sample activity data Then run _python
import_data_to_db.py_. A database will be created in the assets folder.</br>
Commit the new changes</br>
Then run command _git push heroku branch:master_ where branch is the branch you want to deploy