from PIL import Image, ImageDraw, ImageFont, ImageChops
F=lambda s: ImageFont.load_default(size=s)
W,H=1200,630
im=Image.new("RGB",(W,H)); d=ImageDraw.Draw(im)
top=(26,15,46); mid=(90,27,71); bot=(176,58,91)
for y in range(H):
    t=y/H
    c=tuple(int(top[i]+(mid[i]-top[i])*min(t*1.6,1)+(bot[i]-mid[i])*max(0,t-0.6)/0.4) for i in range(3))
    d.line([(0,y),(W,y)],fill=c)
sun=Image.new("RGBA",(420,420),(0,0,0,0)); sd=ImageDraw.Draw(sun)
for y in range(420):
    t=y/420
    if (y%30)<22: sd.line([(0,y),(420,y)],fill=(255,int(210-120*t),int(61+78*t),255))
mask=Image.new("L",(420,420),0); ImageDraw.Draw(mask).ellipse([0,0,419,419],fill=255)
im.paste(sun,(860,330),ImageChops.multiply(sun.getchannel('A'),mask))
d=ImageDraw.Draw(im)
d.rectangle([0,560,W,H],fill=(13,10,20))
d.text((70,70),"GUÍA EN ESPAÑOL",font=F(36),fill=(45,226,201))
d.text((64,140),"GTA 6",font=F(170),fill=(255,255,255),stroke_width=3,stroke_fill=(255,255,255))
d.text((70,350),"Fecha, precio, personajes y mapa",font=F(46),fill=(236,232,245),stroke_width=1,stroke_fill=(236,232,245))
d.text((70,410),"19 nov 2026 · PS5 · Xbox Series X|S",font=F(38),fill=(255,210,61),stroke_width=1,stroke_fill=(255,210,61))
d.text((70,582),"Hora por países · Precio · Personajes · Mapa",font=F(26),fill=(167,159,191))
im.save("static/og.png",optimize=True)
ic=Image.new("RGB",(180,180)); di=ImageDraw.Draw(ic)
for x in range(180): di.line([(x,0),(x,180)],fill=(255,int(61+93*x/180),int(139-78*x/180)))
di.text((90,90),"6",font=F(130),fill=(26,15,46),anchor="mm",stroke_width=4,stroke_fill=(26,15,46))
ic.save("static/apple-touch-icon.png",optimize=True)
