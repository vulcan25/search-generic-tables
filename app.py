# https://stackoverflow.com/questions/59510097/creating-a-browser-tab-that-return-data-from-database-with-flask-template-inher

from flask import Flask, render_template, g, request

from query_builder import CustomQuery

app=Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# A minimal route which returns everything:

@app.route('/')
def index():
  sql = "SELECT * FROM Movies"
  headers, objects = CustomQuery(sql).result()
  return render_template('index.html', headers=headers, objects=objects)

# A route with a search box

@app.route('/search')
def search_result():

    sql = """
      SELECT * FROM Movies 
      WHERE "Lead Studio" = ? COLLATE NOCASE;
    """
    query = request.args.get('query', type=str)
    
    if not query:
        # No query string was supplied, just
        # render the empty template:        
        return render_template('index.html', display_search=True)

    params = (query,)
        
    headers, objects = CustomQuery(sql, params).result()

    return render_template('index.html', headers = headers, objects = objects, display_search=True)


original_items = [{'item 1': "Banana", 'item 2': "Car"}, {'item 1': "Apple", 'item 2': "Bike"}]
items = [ list(v for _,v in x.items()) for x in original_items]


headers = ['item 1','item 2']



@app.route('/all')
def all():
  return render_template('index.html', headers=headers, objects=items)