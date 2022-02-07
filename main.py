from flask import Flask,request
import json,stream_sites

app = Flask(__name__)

@app.route("/",methods=["POST"])
def download():     
    payload = json.loads(request.data)
    main_url = payload["url"]
    hostname = payload["hostname"]
    if "wynk" in hostname:
        return stream_sites.wynk(main_url)
    
    return stream_sites.gaana(main_url,payload["title"])
    
   

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=80,debug=True)


