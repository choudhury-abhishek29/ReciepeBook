# RecipeBook Application

### Description
This is an API application based on Python Flask framework. The application lets you perform the following operations:

- Register a user
- View user profile
- Add a recipe
- Delete a recipe
- Update a recipe
- Search for a recipe

Following is a description of each of the above operations and how to perform them.

#### 1. Register a User
This is the first step to perform before using the application. The _username_ and _password_ are used for all the subsequesnt requests for authentication.

API Endpoint
```POST /signup```

Body
```json
{
    "username": <String>,
    "password": <String>,
    "email": <String>,
    "name": <String>
}
```

Response
```json
signup success : <username>
```

#### 2. View User Profile
This endpoint lists all the recipes which have been added for a user. For this endpoint to work, you need to add the _username_ and _password_ of a registered user.
API Endpoint
```GET /profile```

Authorization
```json
Basic Auth  <username>  <password>
```

Response
```json
[<recipe>, <recipe>, <recipe>]
```

#### 3. Add a recipe
User can add a recipe using this endpoint. For this endpoint to work, you need to add the _username_ and _password_ of a registered user.
API Endpoint
```POST /recipe```

Authorization
```json
Basic Auth  <username>  <password>
```
Body
```json
{
    "category": <any one of ['breakfast', 'lunch', 'dinner']>,
    "ingredients": {
        <string>:{"quantity": <integer/float>, "unit": <any one of valid units of measure>},
        <string>:{"quantity": <integer/float>, "unit": <any one of valid units of measure>},
        <string>:{"quantity": <integer/float>, "unit": <any one of valid units of measure>},
    },
    "instructions": <string>,
    "notes": <string>,
    "recipename": <string>,
    "servingsize": <integer/float>
}

** valid units of measure as of now : ['count', 'gm', 'ml', 'l', 'inch', 'tsp', 'tbsp']. 
This can be updated based on requirements 
```
Response
```json
Recipe added : <recipename>
```

#### 3. Delete a recipe
User can delete a recipe using this endpoint. User will need the _id_ of a recipe which can be found in _User Profile_ or _Recipe Search_ recipe details.

API Endpoint
```DELETE /delete/<id>```

Authorization
```json
Basic Auth  <username>  <password>
```
Response
```json
Recipe Deleted Successfully
```

#### 4. Update a Recipe
User can update a recipe details using this endpoint. The user has the flexibility of updating any details of a recipe, updating ingredient details and add or removing ingredients.
Valid _username_, _password_ and recipe's _id_ is required for this endpoint to work.
API Endpoint
```PUT /update/<id>```

Authorization
```json
Basic Auth  <username>  <password>
```
Response
```json
Recipe updated successfully : <recipename>
```

Following are the different examples of how this endpoint can be used 
* Update recipe details

Body

```json
{
  <any of ['category', 'instructions', 'notes', 'recipename', 'servingsize']>: <string>
}
```
* Update ingredient details

Body

```json
{
  "ingredients": {
        <any existing ingredient>:{"quantity": <integer>, "unit": <string>},
        <any existing ingredient>:{"quantity": <integer>, "unit": <string>}
    }
}
```

* Add new ingredients

Body

```json
{
  "ingredients": {
        <any non existing ingredient>:{"quantity": <integer>, "unit": <string>},
        <any non existing ingredient>:{"quantity": <integer>, "unit": <string>}
    }
}
```

* Remove ingredients

Body

```json
{
  "ingredients": {
        "remove":[<list of any existing ingredients>]
    }
}
```

#### 5. Search a Recipe
User can search a recipe using this endpoint. The search is performed for the recipes added by the logged in user. It doesn't show recipes added by other users.
Valid _username_ and _password_ is required for this endpoint to work.
API Endpoint
```GET /search```

Parameters

Following parameters can be used for searching a recipe : 
```
/search/recipe?category=lunch
/search/recipe?recipename=pizza
/search/recipe?servingsize=2
/search/recipe?id=8
```
Authorization
```json
Basic Auth  <username>  <password>
```
Response
```json
[<recipe>, <recipe>, <recipe>]
```


### Run the RecipeBook Application
1. For downloading and running the code, you should have the following installed on your system:
   * Python 3.8 and above
   * Git or Gitbash
   * pip
2. Checkout code from repository : ```git clone https://github.com/choudhury-abhishek29/ReciepeBook.git```
3. This will create a directory `ReciepeBook`.
4. Go inside the directory `ReciepeBook` and checkout the `master` branch.
    ```
   cd ReciepeBook
   git checkout master
   ```
5. Once you see the files in the directory, run the following command
    ```pip install -r requirements.txt```
    
    This will install all the libraries required to run this project.
6. Once the installation completes, run the following commands to export the Flask application
   ```
   cd ..
   export FLASK_APP=ReciepeBook
   ```
7. Run the application
   ```
   flask run
   ```
   If there are no errors, the application should run successfully and show the following message:
   ```
   * Serving Flask app 'ReciepeBook'
   * Debug mode: off
   WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
   * Running on http://127.0.0.1:5000
   Press CTRL+C to quit
   ```
   The application runs on port 5000 by default. If you want to run the application on a specific port, please run the following command:
   ```
   flask run -p <port_number>
   ```
   
8. To verify the application is running, go to the following URL from a browser or Postman
   ```
   http://127.0.0.1:5000
   ```
   You should see the following response:
   ```
   Welcome to your Recipe Book
   ```