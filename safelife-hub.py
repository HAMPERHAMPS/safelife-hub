from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
safever = 2.0 # Please dont change this. This lets the client know how to communicate with this.
print(f"Running SafeLife Hub V{str(safever)}")
mainhub = True # Please change this to false. This is letting the server know that this is the main server. Other servers use this to update.
# im putting this here to see why a datacenter in califonia is using safelife
#if not mainhub:
#    latestver = requests.get('https://safelifehub.hamperhamps.space/version')
#    if str(latestver) != safever:
#        print("YOU ARE USING AN OLD SERVER VERSION!!! PLEASE GO TO https://github.com/HAMPERHAMPS/safelife-hub/edit/main/safelife-hub.py AND DOWNLOAD THE LATEST SERVER VERSION FOR THE CLIENT TO WORK CORRECTLY!!!")
app = Flask(__name__)
banned = """108.51.114.54 174.219.255.241"""
online = True # I turn this off from time to time to keep me safe from "odd" users. I recommend you do the same sometimes. Once people were doing illegal things with my friend's site... That did not go too well. I am now scared to do anything like this lol. Maybe I shouldn't.
bannedwords = ["porn", "hentai", "drug", "onion", "gov", "silkroad", "darknet", "torrent", "piratebay", "phishing", "malware", "trojan", "keylogger", "extremism", "terrorism", "narcotics", "firearms", "fakeid", "creditcardfraud", "scam", "ponzi", "child", "selfharm", "darkweb"] # add more if you need to
prvurl = ""
CORS(app)
@app.route('/', methods=['GET', 'POST'])
def proxy():
    client_ip = request.remote_addr
    url = request.args.get('url')
    if url == "eshutoff9900":
        
        online = False
    
    if not online:
        webhook_url = 'https://discordapp.com/api/webhooks/1260679944309051434/KfTn6WyuMH1ZEDy5FgvL9YA4AiitqG4o-fFJ2SuUfjY7Ty3BkeX4V-PPtGBgzwF-wKuW'
        payload = {
            
            'content': client_ip + " | REQUEST = OFFLINE"
        }
        json_payload = json.dumps(payload)

        
        response = requests.post(webhook_url, data=json_payload, headers={'Content-Type': 'application/json'})
        return jsonify({
            'status_code': 30023,
            'content': f"""<p style="color: red;">This server is not online. Try a different one. </p> <p>RUNNING SAFELIFE-HUB V{str(safever)} </p> <p style="color: red;">Your current ip: {str(client_ip)}</p>"""
        }) 

    if any(word in url for word in bannedwords):
        webhook_url = 'https://discordapp.com/api/webhooks/1260679944309051434/KfTn6WyuMH1ZEDy5FgvL9YA4AiitqG4o-fFJ2SuUfjY7Ty3BkeX4V-PPtGBgzwF-wKuW'
        payload = {
            
            'content': client_ip + " | " + url + " = BANNED"
        }
        json_payload = json.dumps(payload)

        
        response = requests.post(webhook_url, data=json_payload, headers={'Content-Type': 'application/json'})
        return jsonify({
            'status_code': 30023,
            'content': f"""<p style="color: red;">You are trying to use a banned service. Please dont. </p> <p>RUNNING SAFELIFE-HUB V{str(safever)} </p> <p style="color: red;">Your current ip: {str(client_ip)}</p>"""
        }) 

    if str(client_ip) in banned:
        return jsonify({
            'status_code': 30023,
            'content': f"""<p style="color: red;">Your IP is banned. </p> <p>RUNNING SAFELIFE-HUB V{str(safever)} </p> <p style="color: red;">Your current ip: {str(client_ip)}</p>"""
        }) 
    try:
        
        webhook_url = 'https://discordapp.com/api/webhooks/1260679944309051434/KfTn6WyuMH1ZEDy5FgvL9YA4AiitqG4o-fFJ2SuUfjY7Ty3BkeX4V-PPtGBgzwF-wKuW'
        payload = {
            
            'content': client_ip + " | " + url
        }
        json_payload = json.dumps(payload)

        
        response = requests.post(webhook_url, data=json_payload, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            print('yep')
        else:
            print(f'Failed to send message to Discord webhook. Status code: {response.status_code}')
            print(response.text) 
        if url:
            global prvurl
            if "http" not in url:
                url = prvurl + url
            response = requests.get(url)
            prvurl = url
            return jsonify({
                'status_code': response.status_code,
                'content': response.text
            })

    except Exception as e:
        return jsonify({
            'status_code': 1,
            'content': f"""<p style="color: red;">NYOOOOOoOooOOOo somethings wrong!!! Error: {e}</p> <p>RUNNING SAFELIFE-HUB V{str(safever)} </p> <p style="color: red;">Your current ip: {str(client_ip)}</p>"""
        })

@app.route('/ping', methods=['GET'])
def ping():
    satsts = "ok"
    if online:
        return jsonify({'status': 'ok'})

    
@app.route('/version', methods=['GET'])
def version():
    return jsonify({'ver': safever})

if __name__ == '__main__':
    app.run(debug=True)
