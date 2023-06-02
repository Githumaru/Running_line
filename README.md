# Running Line Video Project

This project is a Django application that generates short videos with a running line and stores the user requests in a MongoDB database.

## Installation

1. Clone the repository to your local machine:

```shell
git clone https://github.com/Githumaru/Running_line.git

2. Navigate to the project's root directory:

cd Running_line

3. Create and activate a virtual environment:

python3 -m venv myenv
source myenv/bin/activate

4. Install the required dependencies using pip:

pip install -r requirements.txt

5. Set up the MongoDB database:

Install MongoDB on your system.
Start the MongoDB service.
Create a new database named datatest.
Make sure you have the necessary permissions and credentials to access the MongoDB server.

6. Perform the database migrations:

python manage.py makemigrations
python manage.py migrate

USAGE
1. Start the development server:

python manage.py runserver

2. Open your web browser and navigate to http://127.0.0.1:8000/app_string/running_line/?text=<text> (replace <text> with the desired running line text).

3. The application will generate a short video with the running line text. The video will be downloaded automatically.

4. The user requests will be stored in the videodata collection of the datatest database in MongoDB.
Each request will include the request time and the text of the running line.

CONTRIBUTION
If you encounter any issues, have suggestions, or would like to contribute to this project, please feel free to open an issue or submit a pull request.
