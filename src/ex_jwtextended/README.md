# Guidance

The code in this example is based on
the [Flask-JWT-Extended documentation](https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage.html)

`pip install flask-jwt-extended httpie`

To login use the terminal with httpie. 
Enter `http POST :5000/login username=panther password=claw`

This will print the access_token to the terminal. Copy the access token then use the commands below.

`export JWT="paste-your-access-token-here"`

`http GET :5000/who_am_i Authorization:"Bearer $JWT"`

This should return JSON with the id and username.

To show the message if login fails enter `http POST :5000/login username=batman password=password`


