import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import graph
from forms import SearchForm
from search import Search

app = Flask(__name__)

# CSRF
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# Forms and template
Bootstrap(app)


# UI ---------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    search_form = SearchForm()
    search_result = None
    volumes_graph = None
    if search_form.validate_on_submit():
        query_symbol = search_form.stock_symbol.data
        if query_symbol.isnumeric():
            search_result = Search(query_symbol).display_data
            if search_result.get("volumes") is not None:
                volumes_graph = graph.to_img(search_result["volumes"])

    return render_template("index.html", form=search_form, result=search_result, graph=volumes_graph)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5301, debug=True)
