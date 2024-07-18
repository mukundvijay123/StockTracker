from flask import Flask,render_template,request,jsonify
import redis
import json

app=Flask(__name__)
redisPort=6379
redisClient=redis.Redis("localhost",redisPort)


@app.route('/',methods=['GET'])
def home():
    return render_template("welcome.html")

@app.route('/submit', methods=['POST'])
def handle_request():
    data = request.json
    button_id = data['buttonId']
    ticker_text = data['tickerText']
    temp={"objType":button_id,"ticker":ticker_text}
    print(temp)
    redisClient.rpush("InputQueue",json.dumps(temp))
    # Process the data as needed
    print(f"Button ID: {button_id}, Ticker Text: {ticker_text}")
    return jsonify({'status': 'success', 'buttonId': button_id, 'tickerText': ticker_text})





if __name__=="__main__":
    app.run(debug=True)
