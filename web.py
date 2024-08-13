from flask import Flask, render_template, request, jsonify
import shelve
import os

def set(key, value):
  with shelve.open('mydb') as db:
      db[key] = value

def get(key):
  with shelve.open('mydb') as db:
      return db.get(key)
    
app = Flask(__name__)

@app.route('/panel', methods=['GET', 'POST'])
def save_items():
    if request.method == 'POST':
      items = request.json
      print("Received items:", items)
      set('items', items)
      return jsonify({"status": "success"})
    elif request.args.get('code') == 'XPAat7my219H2lxT1auHpSyGTNJRhV0c':
      items = get('items')
      return render_template('panel.html', items=items or [])
    return "<h1>404 not found</h1>"

text = '<input class="small_text" name={} placeholder="{}" required>'
textbox = '<span placeholder="{}" class="textarea" role="textbox" contenteditable></span>'
checkbox = '<div class="checkbox"><label>{}</label><input type="checkbox" name={} /></div>'

@app.route('/')
def main():
  items = get('items')
  content = ""
  for item in items:
    if item["type"] == "text":
      content += text.format(item["label"], item["label"])
    elif item["type"] == "textbox":
      content += textbox.format(item["label"])
    elif item["type"] == "checkbox":
      content += checkbox.format(item["label"], item["label"])
    
  return render_template("index.html", content=content)

TEST_USERNAME = "admin"
TEST_PASSWORD = 'lGGN2ZEfmL'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
  if request.method == 'POST':
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username == TEST_USERNAME and password == TEST_PASSWORD:
        return jsonify({"status": "success", "message": 'XPAat7my219H2lxT1auHpSyGTNJRhV0c'}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401
  return render_template("admin.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80, debug=True)