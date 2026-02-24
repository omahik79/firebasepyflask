from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route("/")
def index():
    contacts = db.collection("contacts").stream()
    contact_list = []
    for doc in contacts:
        contact_list.append({**doc.to_dict(), "id": doc.id})
    return render_template("index.html", contacts=contact_list)

@app.route("/add", methods=["POST"])
def add():
    db.collection("contacts").add({
        "firstName": request.form["firstName"],
        "lastName": request.form["lastName"],
        "email": request.form["email"]
    })
    return redirect("/")

@app.route("/delete/<id>")
def delete(id):
    db.collection("contacts").document(id).delete()
    return redirect("/")

if __name__ == "__main__":
    # Use a safe port for Windows to avoid socket issues
    app.run(debug=True, port=8000)
