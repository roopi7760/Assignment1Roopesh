from flask import Flask
app = Flask(__name__)

@app.route("/")
def main():
    execfile("abc.py")
    return add()

if __name__ == "__main__":
    app.run()