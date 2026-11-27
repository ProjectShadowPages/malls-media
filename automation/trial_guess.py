# Trial reel 2: "You'd never guess these are places to shop" (built 27.11.2026)
import sys, os, subprocess
sys.path.insert(0,'/home/claude/malls-media/automation')
import render
from PIL import Image, ImageDraw
W,H=1080,1920; S='/tmp/t2/'; O='/tmp/t2/o/'
Y=(255,214,0); WH=(255,255,255); K=(0,0,0)
scenes=[('villaggio','Venice?','A shopping mall in Doha','Preacher lad, CC BY-SA 4.0'),
        ('g2','A palace?','A shopping mall in Moscow','Bahnfrend, CC BY-SA 4.0'),
        ('dubai','An aquarium?','It\'s inside Dubai Mall','Pravichris, CC BY-SA 4.0'),
        ('milan','A cathedral?','A shopping arcade in Milan','C messier, CC BY-SA 4.0')]
def bg(f):
    im=Image.open(S+f+'.jpg').convert('RGB'); cw,ch=int(W*1.12),int(H*1.12)
    r=max(cw/im.width,ch/im.height); im=im.resize((int(im.width*r)+1,int(im.height*r)+1))
    return im.crop(((im.width-cw)//2,(im.height-ch)//2,(im.width-cw)//2+cw,(im.height-ch)//2+ch))
def ctext(d,y,t,f,col):
    d.text(((W-d.textlength(t,font=f))/2,y),t,font=f,fill=col,stroke_width=5,stroke_fill=K)
def base_ov():
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    for y in range(0,560): d.line([(0,y),(W,y)],fill=(0,0,0,int(150*(1-y/560))))
    for y in range(H-700,H): d.line([(0,y),(W,y)],fill=(0,0,0,int(170*(y-(H-700))/700)))
    logo=Image.open('/home/claude/malls-media/automation/logo.png').convert('RGBA').resize((120,120))
    m=Image.new('L',(120,120),0); ImageDraw.Draw(m).ellipse([0,0,119,119],fill=255); ov.paste(logo,(45,70),m)
    return ov,d
for i,(f,q,a,c) in enumerate(scenes):
    bg(f).save(O+f'bg{i}.jpg',quality=92)
    for st in (0,1):
        ov,d=base_ov()
        if i==0:  # hook line stays on top in scene 1
            ctext(d,230,"YOU'D NEVER GUESS",render.font('ExtraBold',76),WH)
            ctext(d,320,'THESE ARE PLACES TO SHOP',render.font('ExtraBold',62),Y)
        ctext(d,1250,q,render.font('ExtraBold',110),WH)
        if st: ctext(d,1420,a,render.font('ExtraBold',70),Y)
        fc=render.font('Medium',26); t='Photo: '+c+' / Wikimedia Commons'
        d.text(((W-d.textlength(t,font=fc))/2,H-130),t,font=fc,fill=(215,215,215))
        ov.save(O+f'ov{i}_{st}.png')
e=Image.new('RGB',(W,H),(12,12,12)); d=ImageDraw.Draw(e)
logo=Image.open('/home/claude/malls-media/automation/logo.png').convert('RGBA').resize((340,340))
m=Image.new('L',(340,340),0); ImageDraw.Draw(m).ellipse([0,0,339,339],fill=255); e.paste(logo,((W-340)//2,560),m)
f=render.font('ExtraBold',72)
for y,t,col in [(990,'Which one would',WH),(1080,'you visit first?',Y)]: d.text(((W-d.textlength(t,font=f))/2,y),t,font=f,fill=col)
f=render.font('Medium',44); t='A new mall every day'; d.text(((W-d.textlength(t,font=f))/2,1240),t,font=f,fill=(200,200,200))
e.save(O+'end.png')
# video: scene i = 1.5s question + 2.0s answer (scene 0: 2.2 + 2.0)
clips=[]
for i in range(4):
    d0=2.2 if i==0 else 1.5; d1=2.0; tot=d0+d1
    X=f"(iw-1080)*t/{tot}" if i%2==0 else f"(iw-1080)*(1-t/{tot})"
    out=O+f'c{i}.mp4'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-t',str(tot),'-i',O+f'bg{i}.jpg','-loop','1','-t',str(tot),'-i',O+f'ov{i}_0.png','-loop','1','-t',str(tot),'-i',O+f'ov{i}_1.png',
      '-filter_complex',f"[0:v]crop=1080:1920:x='{X}':y='(ih-1920)/2'[b];[b][1:v]overlay=0:0:enable='lt(t,{d0})'[c];[c][2:v]overlay=0:0:enable='gte(t,{d0})',format=yuv420p,fps=30[o]",
      '-map','[o]','-c:v','libx264','-preset','veryfast','-crf','19',out],check=True); clips.append((out,tot))
subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-t','3','-i',O+'end.png','-vf','format=yuv420p,fps=30','-c:v','libx264','-preset','veryfast','-crf','19',O+'c4.mp4'],check=True); clips.append((O+'c4.mp4',3))
fd=0.3; ins=[]; [ins.extend(['-i',c]) for c,_ in clips]; flt='';last='0:v';off=0
for k in range(1,len(clips)):
    off+=clips[k-1][1]-fd; flt+=f'[{last}][{k}:v]xfade=transition=fade:duration={fd}:offset={off:.2f}[v{k}];'; last=f'v{k}'
total=sum(t for _,t in clips)-fd*(len(clips)-1)
mus='/home/claude/malls-media/music/sub_clair-upbeat-571898.mp3'
flt+=f'[{last}]format=yuv420p[o];[{len(clips)}:a]atrim=0:{total:.2f},afade=t=in:d=0.3,afade=t=out:st={total-1.2:.2f}:d=1.2[a]'
os.makedirs('/home/claude/malls-media/media/trial',exist_ok=True)
subprocess.run(['ffmpeg','-y','-loglevel','error',*ins,'-i',mus,'-filter_complex',flt,'-map','[o]','-map','[a]','-r','30','-c:v','libx264','-profile:v','high','-preset','veryfast','-crf','20','-c:a','aac','-b:a','128k','-ar','48000','-ac','2','-movflags','+faststart','/home/claude/malls-media/media/trial/guess-malls-trial.mp4'],check=True)
print(total)
