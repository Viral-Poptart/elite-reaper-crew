import os, json, urllib.request
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont

PLAYER_ID = 2047491
OUT = Path('site'); OUT.mkdir(exist_ok=True)
key = os.environ.get('TORN_API_KEY', '')
status = 'UNKNOWN'
if key:
    try:
        req = urllib.request.Request(f'https://api.torn.com/v2/user/{PLAYER_ID}/profile', headers={'Authorization':f'ApiKey {key}', 'User-Agent':'ERC-Status-Poster/1.0'})
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.load(response)
        if 'error' in data: raise RuntimeError(str(data['error']))
        raw = str((data.get('last_action') or {}).get('status', '')).strip().lower()
        if raw in ('online','idle','offline'): status = raw.upper()
        else: print('Unexpected last_action status; displaying UNKNOWN')
    except Exception as exc:
        print(f'API request failed: {type(exc).__name__}; displaying UNKNOWN')

base = Path('poster.png')
if base.exists():
    im = Image.open(base).convert('RGB')
    # Place status within THE COMMAND box on the reference 1024x1536 layout.
    x, y, w, h = (695, 1105, 215, 39)
    sx, sy = im.width / 1024, im.height / 1536
    x,y,w,h = [round(a*b) for a,b in zip((x,y,w,h),(sx,sy,sx,sy))]
else:
    im = Image.new('RGB',(700,120),(12,10,14))
    x,y,w,h = 20,40,660,55

d = ImageDraw.Draw(im)
d.rounded_rectangle((x,y,x+w,y+h),radius=max(4,h//3),fill=(8,9,12),outline=(150,20,35),width=max(1,h//15))
colors={'ONLINE':(80,235,95),'IDLE':(240,185,55),'OFFLINE':(160,165,175),'UNKNOWN':(185,120,130)}
c=colors[status]
r=max(3,h//7)
d.ellipse((x+12,y+h//2-r,x+12+2*r,y+h//2+r),fill=c)
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=ImageFont.truetype(fontpath,max(12,int(h*.47)))
d.text((x+25+2*r,y+(h-int(h*.47))//2-2),status,font=font,fill=c)
im.save(OUT/'status.png',optimize=True)
(OUT/'status.json').write_text(json.dumps({'player_id':PLAYER_ID,'status':status,'updated_utc':datetime.now(timezone.utc).isoformat()},indent=2))
print('Generated:',status)
