A Flask app which uses `sqlite3` to query the database, and displays it in the frontend with datatables.js.

Implements a class called `query_builder.CustomQuery` to make issuing SQL commands within a route easy:

```
@app.route('/')
def index():
  sql = "SELECT * FROM Movies"
  headers, objects = CustomQuery(sql).result()
  return render_template('index.html', headers=headers, objects=objects)
```

This automatically generates the header rows, so the template code is kept generic (no hard coding of header names in the table. Yay!).

There's also a `/search` route, which can be used to filter the table based on a predefined SQL query:

```
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
```
This is slightly redundant due to datatables having a built in search bar, but demonstrates how to pass parameters to your SQL query.

References
==========

- Best practice for SQL queries: https://www.btelligent.com/en/blog/best-practice-for-sql-statements-in-python/