from flask import Flask, render_template, request, redirect, url_for, flash
import os
import csv

app = Flask(__name__)
app.secret_key = "secret-key"

# Ensure the 'profiles' directory exists
if not os.path.exists("profiles"):
    os.makedirs("profiles")

# Ensure the 'Profiles.csv' file exists
if not os.path.exists("Profiles.csv"):
    with open("Profiles.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Email", "Phone", "Website", "Headshot Path"])


@app.route("/")
def landing_page():
    return render_template("index.html")


@app.route("/create-profile", methods=["GET", "POST"])
def create_profile():
    if request.method == "POST":
        # Get user data from the form
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        website = request.form["website"]
        headshot = request.files["headshot"]

        # Generate a folder name from the user's name
        folder_name = name.replace(" ", "_")
        user_folder = os.path.join("profiles", folder_name)

        # Create a folder for the user's profile if it doesn't exist
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        # Save the headshot in the user's folder
        headshot_path = os.path.join(user_folder, "headshot.jpg")
        headshot.save(headshot_path)

        # Append the user's data to the 'Profiles.csv' file
        with open("Profiles.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, email, phone, website, headshot_path])

        # Save profile data as a JSON-like structure
        profile_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "website": website,
            "headshot": headshot_path,
        }

        # Save profile data to a JSON file
        profile_json_path = os.path.join(user_folder, "profile.json")
        with open(profile_json_path, "w") as jsonfile:
            json.dump(profile_data, jsonfile)

        flash("Profile created successfully!")
        return redirect(url_for("view_profile", name=folder_name))

    return render_template("form.html")


@app.route("/profile/<name>")
def view_profile(name):
    # Retrieve the user's profile folder
    user_folder = os.path.join("profiles", name)

    # Check if the folder exists
    if not os.path.exists(user_folder):
        return "Profile not found!", 404

    # Load profile data
    profile_json_path = os.path.join(user_folder, "profile.json")
    with open(profile_json_path, "r") as jsonfile:
        profile_data = json.load(jsonfile)

    return render_template("profile.html", user=profile_data)


if __name__ == "__main__":
    app.run(debug=True)
