from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = "123"
db_name = "website.db"


# Main Homepage
@app.route('/')
@app.route('/index')
def index():  # put application's code here

    # Get all categories to display on the homepage for search
    categories = get_categories()
    return render_template("index.html", categories=categories)


# Register page
@app.route('/register')
def register():
    return render_template("register.html")


# Register the user via post request
@app.route("/register_user", methods=["GET", "POST"])
def register_user():
    # If the user submits the form using POST
    if request.method == "POST":
        # Get the form data
        username = request.form["username"]
        password = request.form["password"]
        fullname = request.form["fullname"]
        email = request.form["email"]
        telephone = request.form["telephone"]

        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        # Check if the username already exists
        c.execute("SELECT * FROM User WHERE username=?", (username,))
        if len(c.fetchall()) > 0:
            conn.close()
            # If the username already exists, then redirect to /register with an error message
            return render_template("register.html", msg="Username already exists")

        # Insert the user into the database
        c.execute("INSERT INTO User VALUES(?,?,?,?,?)", (username, password, fullname, email, telephone))
        conn.commit()
        conn.close()

        # Create a session for the user and redirect to /confirmation_site
        session["username"] = username
        return redirect(url_for("confirmation_site"))

    # If the user directly goes to /register_user, then redirect to /register (tries get method)
    return redirect(url_for("register"))


# Confirmation site
@app.route('/confirmation_site')
def confirmation_site():
    # If the user is logged in, then display the confirmation site with the username
    if "username" in session:
        return render_template("confirmation_site.html", username=session["username"])
    else:
        return render_template("confirmation_site.html")


# Login page
@app.route('/login_user', methods=["GET", "POST"])
def login_user():
    # If the user submits the form using POST
    if request.method == "POST":
        # Get the form data
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        # Check if the username and password match
        c.execute("SELECT * FROM User WHERE username=? AND password=?", (username, password))
        users = c.fetchall()
        conn.close()

        # If the username and password match, then redirect to homepage
        if len(users) == 1:
            # Create a session for the user and redirect to homepage
            session["username"] = username
            return redirect(url_for("index"))
        else:
            # If the username and password do not match, then redirect to /login with an error message
            return render_template("index.html", login_error="Login failed", categories=get_categories())

    # If the user directly goes to /login_user, then redirect to /login (tries get method)
    return redirect(url_for("index"))


# Logout
@app.route("/logout")
def logout():
    # Remove the username from the session if it is there
    session.pop("username", None)
    return redirect(url_for('index'))


# User advertisements
@app.route('/user_advertisements')
def user_advertisements():
    # If the user is logged in, then display the user advertisements page
    if "username" in session:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        # Get all advertisements of the user
        c.execute("SELECT * FROM Advertisement WHERE username=?", (session["username"],))
        advertisements = c.fetchall()
        conn.close()

        # Get all categories
        categories = get_categories()
        categories_dict = dict(categories)

        # Replace the category id with the category name
        for i in range(len(advertisements)):
            adv = list(advertisements[i])
            adv[5] = categories_dict[adv[5]]
            advertisements[i] = tuple(adv)

        # If the user is logged in, then show the page with the advertisements
        return render_template("user_advertisements.html", categories=categories, advertisements=advertisements)
    else:
        # If the user is not logged in, then show the page with error message
        return render_template("user_advertisements.html")


# Add advertisement
@app.route('/add_advertisement', methods=["GET", "POST"])
def add_advertisement():
    # If the user is logged in, then display the add advertisement page
    if "username" in session:
        # If the user submits the form using POST
        if request.method == "POST":
            # Get the form data
            title = request.form["title"]
            description = request.form["description"]
            category = request.form["category"]

            conn = sqlite3.connect(db_name)
            c = conn.cursor()

            # Insert the advertisement into the database
            c.execute("INSERT INTO Advertisement(title, description, isactive, username, cid) VALUES(?,?,?,?,?)",
                      (title, description, True, session["username"], category))
            conn.commit()
            conn.close()

        # Show the add advertisement page with newly added advertisement
        return redirect(url_for("user_advertisements"))
    return redirect(url_for("index"))


# Deactive advertisement
@app.route('/deactivate_advertisement', methods=["GET", "POST"])
def deactivate_advertisement():
    # If the user is logged in, then process the deactivation
    if "username" in session:
        if request.method == "POST":
            # Get the form data
            aid = request.form["aid"]

            conn = sqlite3.connect(db_name)
            c = conn.cursor()

            # Deactivate the advertisement
            c.execute("UPDATE Advertisement SET isactive=? WHERE aid=? AND username=?",
                      (False, aid, session["username"]))
            conn.commit()
            conn.close()
        # Show the user advertisements page with the deactivated advertisement
        return redirect(url_for("user_advertisements"))
    return redirect(url_for("index"))


# Activate advertisement
@app.route('/activate_advertisement', methods=["GET", "POST"])
def activate_advertisement():
    # If the user is logged in, then process the activation
    if "username" in session:
        # If the user submits the form using POST
        if request.method == "POST":
            # Get the form data
            aid = request.form["aid"]

            conn = sqlite3.connect(db_name)
            c = conn.cursor()

            # Activate the advertisement
            c.execute("UPDATE Advertisement SET isactive=? WHERE aid=? AND username=?",
                      (True, aid, session["username"]))
            conn.commit()
            conn.close()

        # Show the user advertisements page with the activated advertisement
        return redirect(url_for("user_advertisements"))
    return redirect(url_for("index"))


# Profile Page
@app.route('/profile')
def profile():
    # If the user is logged in, then display the profile page
    if "username" in session:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        # Get the user information
        c.execute("SELECT * FROM User WHERE username=?", (session["username"],))
        user = c.fetchone()
        conn.close()

        # Show the profile page with the user information
        return render_template("profile.html", user=user)
    else:
        return render_template("profile.html")


# Edit Profile Page
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    # If the user is logged in, then display the edit profile page
    if "username" in session:
        # If the user submits the form using POST
        if request.method == "POST":
            # Get the form data
            username = request.form["username"]
            password = request.form["password"]
            fullname = request.form["fullname"]
            email = request.form["email"]
            telephone = request.form["telephone"]

            conn = sqlite3.connect(db_name)
            c = conn.cursor()

            # Check if the username already exists
            if session["username"] != username:
                c.execute("SELECT * FROM User WHERE username=?", (username,))
                if len(c.fetchall()) > 0:
                    print("Username already exists")
                    conn.close()
                    # If the username already exists, then redirect to /profile with an error message
                    return render_template("profile.html", user=(username, password, fullname, email, telephone),
                                           error="Username already exists")

            # Delete the user from the database incase the username is changed
            c.execute("DELETE FROM User WHERE username=?", (username,))
            conn.commit()
            # Remove the username from the session if it is there
            session.pop("username", None)

            # Insert the user into the database
            c.execute("INSERT INTO User VALUES(?,?,?,?,?)", (username, password, fullname, email, telephone))
            conn.commit()
            conn.close()

            # Create a session for the user and redirect to /profile
            session["username"] = username
            # Show the profile page with the user information
            return render_template("profile.html", user=(username, password, fullname, email, telephone),
                                   msg="Successfully edited profile!")
        return redirect(url_for("profile"))
    return redirect(url_for("index"))


# Search the advertisements
@app.route('/search', methods=["GET", "POST"])
def search():
    # If the user submits the form using POST
    if request.method == "POST":
        # Get the form data
        search = request.form["search"]
        category = request.form["category"]

        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        # Get all advertisements that match the search query
        categories = get_categories()
        # to_display is the list of categories to display on the homepage
        to_display = []

        # If the category is not all, then search only in that category
        if category != "all":
            c.execute("SELECT * FROM Advertisement INNER JOIN User on Advertisement.username = User.username WHERE "
                      "(title LIKE ? OR description LIKE ? OR fullname LIKE ?) AND cid=? AND isactive=1",
                      ("%" + search + "%", "%" + search + "%", "%" + search + "%", category))
        else:
            c.execute("SELECT * FROM Advertisement INNER JOIN User on Advertisement.username = User.username WHERE "
                      "(title LIKE ? OR description LIKE ? OR fullname LIKE ?) AND isactive=1",
                      ("%" + search + "%", "%" + search + "%", "%" + search + "%"))

        advertisements = c.fetchall()
        conn.close()

        # search_categories is the dictionary of categories to display on the homepage
        search_categories = {}
        categories_dict = dict(categories)
        # Replace the category id with the category name
        for category_id, category_name in categories:
            search_categories[category_name] = []
            if category == "all" or str(category) == str(category_id):
                to_display.append(category_name)

        # Add the data to the search_categories dictionary
        for adv in advertisements:
            aid = adv[0]
            title = adv[1]
            description = adv[2]
            fullname = adv[8]
            category_result = [aid, title, description, fullname]
            search_categories[categories_dict[adv[5]]].append(category_result)

        # Show the homepage with the search results
        return render_template("index.html", search_categories=search_categories, categories=categories,
                               to_display=to_display)

    return redirect(url_for("index"))

# View advertisement
@app.route('/view_advertisement/', methods=["GET", "POST"])
# @app.route('/view_advertisement/<aid>')
def view_advertisement():

    # If the user submits the form using GET
    if request.method == "GET":
        # Get the data
        aid = request.args.get("aid")

        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        # Get the advertisement
        c.execute("SELECT * FROM Advertisement INNER JOIN User on Advertisement.username = User.username WHERE aid=?",
                  (aid,))
        advertisement = c.fetchone()
        conn.close()

        # If the advertisement is not found, then show the error message
        if advertisement is None:
            return render_template("view_advertisement.html", error="Advertisement not found")
        # If the advertisement is not active, then show the error message
        if not advertisement[3]:
            return render_template("view_advertisement.html", error="Advertisement is not active")

        # Show the advertisement
        data = [advertisement[1], advertisement[2], dict(get_categories())[advertisement[5]], advertisement[8],
                advertisement[9], advertisement[10]]
        return render_template("view_advertisement.html", data=data)
    return render_template("view_advertisement.html", error="Advertisement not found")


# Get all categories
def get_categories():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT * FROM Category")
    categories = c.fetchall()
    conn.close()

    return categories


if __name__ == '__main__':
    app.run()
