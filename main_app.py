from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'dev'  # zmienić na bezpieczny klucz w produkcji

# Basic routes
@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/user_login')
def user_login():
    return render_template('user_login.html')

@app.route('/user_register')
def user_register():
    return render_template('user_register.html')

if __name__ == '__main__':
    app.run(debug=True)