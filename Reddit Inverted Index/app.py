from flask import Flask
from flask import request
import main
import flask
app = Flask(__name__)




@app.route('/execute_query',methods=['Get','POST'])
def execute_query():
      
    # GET THE SQLALCHEMY RESULTPROXY OBJECT

    queries = request.json["queries"]

    responseBody =main.getResponse(queries)
    
  
    return responseBody    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)