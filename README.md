# SE-Project Setup Guide

This guide provides comprehensive instructions for setting up the SE-Project from scratch, including both frontend (Vue.js) and backend (Flask) components.

## Prerequisites

Ensure you have the following installed on your system:

- [Git](https://git-scm.com/downloads)
- [Node.js](https://nodejs.org/) (LTS version recommended)
- [npm](https://www.npmjs.com/) (included with Node.js)
- [Python](https://www.python.org/downloads/) (version 3.8 or higher)

## 1. Clone the Repository

```
git clone [https://github.com/Sparkonix11/Knowtopia.git]
cd SE-Project
```

## 2. Frontend Setup (Vue.js)

### Install Node.js Dependencies

```
npm install
```

This will install all the required frontend dependencies listed in package.json, including:
- Vue.js and Vue Router
- Axios for API requests
- Chart.js for data visualization
- Tailwind CSS for styling

## 3. Backend Setup (Flask)

### Create a Python Virtual Environment

#### For Windows:

```
cd server
python -m venv myenv
myenv\Scripts\activate
```

#### For macOS/Linux:

```
cd server
python3 -m venv myenv
source myenv/bin/activate
```

### Install Python Dependencies

With the virtual environment activated:

```
pip install -r requirements.txt
```

This will install all the required backend dependencies, including:
- Flask and Flask extensions (Flask-RESTful, Flask-SQLAlchemy, Flask-Migrate, etc.)
- OpenAI libraries
- Database tools
- Testing libraries

### Configure Environment Variables

1. Create a .env file in the server directory by copying the example file:

```
copy .env.example .env  # For Windows
# OR
cp .env.example .env    # For macOS/Linux
```

2. Open the .env file and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```


## 4. Create Mock Data (Optional)

The project includes a script to create sample data for testing purposes:

1. Ensure the Flask server is running in a separate terminal:

```
# In the server directory with virtual environment activated
python app.py
```

2. In another terminal, run the mock data creation script:

```
# In the server directory with virtual environment activated
python create_mock_data.py
```

This script will create:
- Sample users (instructor and student)
- A sample course with materials
- Sample assignments and other data

## 5. Running the Application

### Option 1: Run Frontend and Backend Separately

#### Terminal 1 - Backend (Flask):

```
cd server
myenv\Scripts\activate  # For Windows
# OR
source myenv/bin/activate  # For macOS/Linux
python app.py
```

The Flask server will run at http://127.0.0.1:5000

#### Terminal 2 - Frontend (Vue.js):

```
npm run dev
```

The Vue development server will run at http://localhost:5173 (or another port if 5173 is in use)

### Option 2: Run Both with Concurrently(If you are using Windows and your server virtual env is named as "myenv")

The project includes a script to run both frontend and backend simultaneously:

```
npm run start
```

## 6. Docker Setup (Alternative)

The project also includes Docker configuration for containerized deployment:

```
docker-compose up --build
```

This will build and start both the frontend and backend containers.

## 7. Accessing the Application

Once the application is running, you can access it at:
- Frontend: http://localhost:5173 (or the port shown in your terminal)
- Backend API: http://localhost:5000/api/v1

## 8. Default User Credentials

If you've created mock data, you can log in with these credentials:

- Instructor: instructor@mail.com / password@123
- Student: student@mail.com / password@123

## Troubleshooting

- If you encounter any dependency issues, ensure you're using the correct versions of Node.js and Python.
- For backend errors, check that your virtual environment is activated and all dependencies are installed.
- For database issues, you may need to delete the migrations folder and the database file, then re-initialize the database.
- Ensure the .env file is properly configured with your OpenAI API key.

## Additional Resources

- Vue.js Documentation: https://vuejs.org/guide/introduction.html
- Flask Documentation: https://flask.palletsprojects.com/
- Tailwind CSS Documentation: https://tailwindcss.com/docs
