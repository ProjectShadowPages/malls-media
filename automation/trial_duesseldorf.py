import sys, subprocess, os
sys.path.insert(0,'/home/claude/malls-media/automation')
import render
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
W,H=1080,1920; D='/tmp/dus/'; T='/tmp/trial'; os.makedirs(T,exist_ok=True)
Y=(255,214,0); WH=(255,255,255)
shots=[
 ("Düsseldorf_Arcaden_abenddämmerung.JPG",["THIS GERMAN MALL","HAS A *SWIMMING POOL","INSIDE"],"…and a city library 🇩🇪".replace(" 🇩🇪","")),
 ("Düsseldorf_Arcaden.JPG",["*JUNE 2008","Rising on an old","freight yard"],None),
 ("Düsseldorf_Arcaden-Bau.jpg",["*AUGUST 2008","Inside: still sand","and cables"],None),
 ("Düsseldorf_arcaden_abendbild.jpg",["*SEPTEMBER 2008","Days before","opening day"],None),
 ("Düsseldorf_Arcaden_Abend_Weihnachtsbeleuchtung_2008.jpg",["*CHRISTMAS 2008","The whole façade","lights up"],None),
 ("Düsseldorf_Arcaden_3.jpg",["*TODAY","About 120 shops,","a pool and a library","under one roof"],None),
]
credits=["Michael Driesch","Marek Gehrmann, CC BY-SA 3.0","Michael Driesch","Michael Driesch","Michael Driesch","Joschi71, CC BY-SA 4.0"]
def frame(fn,lines,sub,cred,i):
    im=Image.open(D+fn).convert('RGB')
    # 9:16 big canvas (1.15x for Ken Burns)
    S=1.15; cw,ch=int(W*S),int(H*S)
    r=max(cw/im.width,ch/im.height); bg=im.resize((int(im.width*r)+1,int(im.height*r)+1))
    bg=bg.crop(((bg.width-cw)//2,(bg.height-ch)//2,(bg.width-cw)//2+cw,(bg.height-ch)//2+ch))
    bg.save(f'{T}/bg{i}.jpg',quality=92)
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    # dark gradient bottom
    for y in range(H//2,H): d.line([(0,y),(W,y)],fill=(0,0,0,int(200*(y-H//2)/(H//2))))
    for y in range(0,420): d.line([(0,y),(W,y)],fill=(0,0,0,int(120*(1-y/420))))
    f1=render.font('ExtraBold',78 if i==0 else 80)
    yy=1180 if len(lines)<4 else 1100
    for ln in lines:
        col=Y if ln.startswith('*') else WH; t=ln.lstrip('*')
        if '*' in t: pass
        if i==0 and 'SWIMMING' in ln:
            a,b='HAS A ','SWIMMING POOL'; x=(W-d.textlength(a+b,font=f1))/2
            d.text((x,yy),a,font=f1,fill=WH,stroke_width=4,stroke_fill=(0,0,0)); d.text((x+d.textlength(a,font=f1),yy),b,font=f1,fill=Y,stroke_width=4,stroke_fill=(0,0,0))
        else:
            d.text(((W-d.textlength(t,font=f1))/2,yy),t,font=f1,fill=col,stroke_width=4,stroke_fill=(0,0,0))
        yy+=110
    if sub:
        f2=render.font('Medium',54); d.text(((W-d.textlength(sub,font=f2))/2,yy+20),sub,font=f2,fill=WH,stroke_width=3,stroke_fill=(0,0,0))
    fc=render.font('Medium',26); c='Photo: '+cred+' / Wikimedia Commons'
    d.text(((W-d.textlength(c,font=fc))/2,H-150),c,font=fc,fill=(210,210,210))
    logo=Image.open('/home/claude/malls-media/automation/logo.png').convert('RGBA').resize((130,130))
    mask=Image.new('L',(130,130),0); ImageDraw.Draw(mask).ellipse([0,0,129,129],fill=255)
    ov.paste(logo,(45,70),mask)
    fl=render.flag({'h':[[0,0,0],[221,0,0],[255,206,0]]},120,80).convert('RGBA'); ov.paste(fl,(W-165,95))
    ImageDraw.Draw(ov).rectangle([W-167,93,W-44,176],outline=WH,width=3)
    ov.save(f'{T}/ov{i}.png')
for i,(fn,l,s) in enumerate(shots): frame(fn,l,s,credits[i],i)
# end card
e=Image.new('RGB',(W,H),(12,12,12)); d=ImageDraw.Draw(e)
logo=Image.open('/home/claude/malls-media/automation/logo.png').convert('RGBA').resize((360,360))
mask=Image.new('L',(360,360),0); ImageDraw.Draw(mask).ellipse([0,0,359,359],fill=255); e.paste(logo,((W-360)//2,560),mask)
f=render.font('ExtraBold',72); t='Would you swim'; d.text(((W-d.textlength(t,font=f))/2,1010),t,font=f,fill=WH)
t='before shopping?'; d.text(((W-d.textlength(t,font=f))/2,1100),t,font=f,fill=Y)
f=render.font('Medium',44); t='A new mall every day'; d.text(((W-d.textlength(t,font=f))/2,1260),t,font=f,fill=(200,200,200))
e.save(f'{T}/end.png')
