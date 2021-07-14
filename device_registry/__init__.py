from flask import Flask
import os
import markdown
app = Flask(__name__)

@app.route("/")
def index():
    """Some Documentation"""

    # Open the ReadMe File
    with open(os.path.dirname(app.root_path) + '/ReadMe.md', 'r' ) as markdown_file:
        content = markdown_file.read()

        return markdown.markdown(content)