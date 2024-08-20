from flask import Flask, render_template, redirect, url_for, flash, session, request
import boto3
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your own secret key
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # JWT Secret Key

# Initialize JWT Manager
jwt = JWTManager(app)

# Cognito Config
COGNITO_POOL_ID = "us-east-1_0buFz5iOK"
COGNITO_CLIENT_ID = "6p39b0shsjjhfe6l61eqnn539l"
COGNITO_REGION = "us-east-1"

# Initialize Cognito Client
client = boto3.client('cognito-idp', region_name=COGNITO_REGION)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Authenticate with Cognito
        try:
            response = client.initiate_auth(
                ClientId=COGNITO_CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password,
                },
            )
            session['username'] = username
            access_token = response['AuthenticationResult']['AccessToken']
            id_token = response['AuthenticationResult']['IdToken']

            # Create JWT for session management
            access_jwt = create_access_token(identity=username)
            session['access_jwt'] = access_jwt

            flash('Login successful!', 'success')
            return redirect(url_for('home'))

        except client.exceptions.NotAuthorizedException:
            flash('Incorrect username or password', 'danger')
        except client.exceptions.UserNotFoundException:
            flash('User does not exist', 'danger')

    return render_template('login.html')

# Home Route
@app.route('/')
@jwt_required()
def home():
    current_user = get_jwt_identity()
    return f'Welcome {current_user} to the Home Page!'

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
