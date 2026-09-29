"""Self-referential Bravado pitch film. Original type, motion, and synthesized sound."""
from pathlib import Path
import argparse, json, math, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from render import font, ease, smooth, clamp, rgb, mix

W,H,S,FPS,DURATION=1920,1080,1.5,30,31
CUTS=[0,3,7.5,12,17.5,23,27,31]
BRIEF=json.loads((Path(__file__).with_suffix('.json')).read_text())
P=BRIEF['design']; INK=P['ink']; PAPER=P['paper']; VIOLET=P['violet']; LIME=P['lime']; GRAY=P['gray']; WHITE=P['white']

class Art:
    def __init__(self,bg=INK):
        self.im=Image.new('RGB',(W,H),bg);self.d=ImageDraw.Draw(self.im)
    def rect(self,x1,y1,x2,y2,fill,outline=None,r=0,width=1):
        self.d.rounded_rectangle(tuple(round(v*S) for v in (x1,y1,x2,y2)),radius=round(r*S),fill=fill,outline=outline,width=round(width*S))
    def line(self,points,fill,width=1):
        self.d.line([(round(x*S),round(y*S)) for x,y in points],fill=fill,width=max(1,round(width*S)),joint='curve')
    def circle(self,x,y,r,fill,outline=None,width=1):
        self.d.ellipse(tuple(round(v*S) for v in (x-r,y-r,x+r,y+r)),fill=fill,outline=outline,width=round(width*S))
    def text(self,x,y,string,size=28,color=WHITE,kind='bold',anchor=None):
        self.d.text((round(x*S),round(y*S)),string,font=font(size,kind),fill=color,anchor=anchor)
    def label(self,x,y,string,color=GRAY,size=12,anchor=None):
        self.text(x,y,string,size,color,'mono',anchor)
    def reveal(self,x,y,string,t,at=0,size=72,color=WHITE,kind='heavy',duration=.55):
        p=ease((t-at)/duration)
        if p<=0:return
        f=font(size,kind); height=round(size*1.32*S)
        layer=Image.new('RGBA',(W,height));d=ImageDraw.Draw(layer)
        d.text((0,round((1-p)*height)),string,font=f,fill=color)
        self.im.paste(layer,(round(x*S),round(y*S)),layer)
    def marker(self,t,section,dark=True):
        fg=PAPER if dark else INK; muted=GRAY if dark else '#68707C'
        self.label(58,42,'B / BRAVADO',fg,13)
        self.label(1222,43,section.upper(),muted,11,'ra')
        self.rect(58,675,1222,676,mix(INK,PAPER,.2) if dark else '#D2D4D2')
        self.rect(58,675,58+1164*t/31,677,VIOLET)
        self.label(58,686,'A PRODUCT FILM ABOUT PRODUCT FILMS',muted,10)
        self.label(1222,686,f'{t:05.2f} / 31.00',muted,10,'ra')

def arrow(c,x1,y1,x2,y2,p,color=VIOLET,width=3):
    if p<=0:return
    xe=x1+(x2-x1)*p;ye=y1+(y2-y1)*p
    c.line([(x1,y1),(xe,ye)],color,width)
    if p>.96:c.line([(xe-12,ye-8),(xe,ye),(xe-12,ye+8)],color,width)

def scene0(t,u):
    c=Art()
    c.rect(0,0,14,720,VIOLET)
    for i in range(8):
        x=750+i*70;y=-120+i*72+u*80
        c.line([(x,y),(x+430,y+370)],mix(INK,VIOLET,.12+i*.025),1)
    c.reveal(62,110,'YOU BUILT IT.',u,.24,104,PAPER)
    c.reveal(62,238,'YOU SHIPPED IT.',u,.66,104,LIME)
    p=ease((u-1.1)/.7)
    c.rect(64,422,64+950*p,425,VIOLET)
    if u>1.25:c.reveal(66,469,'NOW SHOW THE WORK.',u,1.24,34,PAPER,'body')
    c.marker(t,'01 / THE HOOK');return c

def scene1(t,u):
    c=Art(PAPER);c.marker(t,'02 / THE GAP',False)
    c.reveal(60,91,'THE WORK IS REAL.',u,.08,79,INK)
    c.reveal(60,185,'MAKE IT FELT.',u,.23,79,VIOLET)
    x=65;y=370
    c.rect(x,y,x+383,y+211,WHITE,'#D7D9DA',11)
    c.rect(x+22,y+21,x+361,y+47,INK,r=5)
    c.circle(x+38,y+34,4,LIME)
    c.label(x+23,y+71,'PROJECT  /  LIVE',INK)
    c.rect(x+23,y+105,x+210,y+117,'#B9BEC6',r=3)
    c.rect(x+23,y+129,x+305,y+138,'#D8DADF',r=3)
    c.rect(x+23,y+150,x+273,y+159,'#D8DADF',r=3)
    c.label(x+23,y+185,'SITE OR GITHUB REPOSITORY',GRAY,10)
    p=ease((u-.8)/1.05)
    arrow(c,463,474,652,474,p)
    words=[('PRODUCT','what it does'),('VISUALS','what it looks like'),('STORY','why it matters')]
    for i,(title,sub) in enumerate(words):
        q=ease((u-1.38-i*.29)/.55);xx=689+(1-q)*70;yy=346+i*81
        if q>0:
            c.rect(xx,yy,1179,yy+67,INK,r=6)
            c.rect(xx,yy,xx+5,yy+67,VIOLET)
            c.text(xx+20,yy+7,title,22,PAPER)
            c.label(xx+200,yy+24,sub.upper(),LIME,10)
    c.label(66,610,'FROM A SHIPPED PROJECT TO A STORY PEOPLE CAN SEE',INK,12)
    return c

def scene2(t,u):
    c=Art();c.marker(t,'03 / THE INPUT')
    c.reveal(61,101,'START WITH A LINK.',u,.1,84,PAPER)
    c.label(65,242,'YOUR SITE OR REPOSITORY',LIME,13)
    c.rect(64,285,1216,375,'#242B39','#596070',9)
    c.rect(79,301,88,359,VIOLET,r=3)
    c.text(110,305,'https://your-project.example',33,PAPER,'mono')
    cursor=ease((u-.44)/1.05)
    c.rect(111+630*cursor,317,114+630*cursor,347,LIME)
    for i,(num,title) in enumerate([('01','SOURCE'),('02','PRODUCT'),('03','VISUAL CUES')]):
        x=64+i*395;q=ease((u-1.55-i*.28)/.65)
        if q<=0:continue
        c.rect(x,451,x+365,563,mix(INK,VIOLET,.12*q),'#52596A',7)
        c.label(x+19,472,num,LIME)
        c.text(x+64,463,title,22,PAPER)
        c.rect(x+19,523,x+19+311*q,525,VIOLET)
    c.label(65,617,'THE AGENT READS THE ACTUAL PROJECT BEFORE WRITING THE FILM',GRAY,11)
    return c

def scene3(t,u):
    c=Art(PAPER);c.marker(t,'04 / THE CRAFT',False)
    c.reveal(60,85,'TYPE.',u,.04,95,INK)
    c.reveal(392,85,'MOTION.',u,.36,95,VIOLET)
    c.reveal(844,85,'SOUND.',u,.7,95,INK)
    c.label(62,242,'ONE PLAYHEAD. EVERY ELEMENT IN TIME.',INK,13)
    c.rect(64,305,1216,550,INK,r=9)
    for i,(name,col) in enumerate([('TYPE',PAPER),('PATH',VIOLET),('AUDIO',LIME)]):
        y=340+i*65
        c.label(87,y+15,name,col,12)
        c.rect(185,y+5,1179,y+7,'#424956')
        if i==0:
            for j in range(4):
                xx=209+j*210;c.rect(xx,y-8,xx+150,y+26,mix(INK,col,.24),r=4)
        elif i==1:
            pts=[]
            for k in range(150):
                x=196+k*6.43;pts.append((x,y+6-18*math.sin(k/23)*math.sin(k/48)))
            c.line(pts,col,3)
        else:
            for j in range(85):
                x=198+j*11.5;amp=(3+21*abs(math.sin(j*.52)*math.sin(j*.19)))
                c.line([(x,y+5-amp),(x,y+5+amp)],col,2)
    p=ease((u-.2)/4.2);px=190+p*983
    c.line([(px,326),(px,525)],LIME,3)
    c.circle(px,306,8,VIOLET)
    c.label(66,601,'MASKED REVEALS  /  CAUSAL DIAGRAMS  /  SYNCHRONIZED CUES',INK,11)
    return c

def scene4(t,u):
    c=Art();c.marker(t,'05 / THE STORY')
    c.reveal(60,88,'SEVEN SCENES.',u,.04,83,PAPER)
    c.reveal(60,185,'ONE CLEAR STORY.',u,.26,83,LIME)
    labels=['HOOK','PROBLEM','SHIFT','MECHANISM','FLOW','PROOF','BRAND']
    for i,label in enumerate(labels):
        x=62+i*166;q=ease((u-.55-i*.34)/.62)
        if q<=0:continue
        y=366+(1-q)*75
        col=VIOLET if i in (0,6) else '#283043'
        c.rect(x,y,x+149,y+177,col,outline='#5C6473',r=7)
        c.label(x+14,y+14,f'{i+1:02}',LIME)
        if i==0:
            c.rect(x+17,y+58,x+119,y+70,PAPER,r=2);c.rect(x+17,y+80,x+99,y+92,LIME,r=2)
        elif i==6:
            c.text(x+18,y+50,'B',64,PAPER,'heavy')
        else:
            c.circle(x+74,y+80,24,None,VIOLET,3)
            c.line([(x+33,y+118),(x+116,y+118)],LIME,2)
        c.label(x+14,y+146,label,PAPER,10)
    c.label(65,614,'A SHORT ARC WITH A JOB FOR EVERY BEAT',GRAY,12)
    return c

def scene5(t,u):
    c=Art(PAPER);c.marker(t,'06 / THE OUTPUT',False)
    c.reveal(60,86,'READY TO SHOW.',u,.1,89,INK)
    c.label(65,243,'A REVIEWABLE CUT, WITH THE PARTS TO KEEP SHAPING IT',INK,13)
    cards=[('STORYBOARD','Seven-scene review'),('EDITABLE SOURCE','Brief + renderer'),('FINISHED MP4','Motion + original audio')]
    for i,(title,sub) in enumerate(cards):
        x=65+i*397;q=ease((u-.56-i*.32)/.58)
        if q<=0:continue
        yy=315+(1-q)*84
        c.rect(x,yy,x+365,yy+260,WHITE,'#D3D5D4',9)
        c.rect(x+16,yy+16,x+349,yy+171,INK,r=5)
        if i==0:
            for j in range(7):c.rect(x+29+(j%4)*77,yy+32+(j//4)*63,x+89+(j%4)*77,yy+79+(j//4)*63,VIOLET if j==0 else '#343D52',r=3)
        elif i==1:
            for j,w in enumerate([185,246,160,229]):c.rect(x+39,yy+44+j*25,x+39+w,yy+49+j*25,LIME if j==0 else '#7881A0',r=2)
        else:
            c.circle(x+184,yy+95,42,VIOLET)
            c.d.polygon([(round((x+174)*S),round((yy+73)*S)),(round((x+174)*S),round((yy+117)*S)),(round((x+209)*S),round((yy+95)*S))],fill=PAPER)
        c.label(x+17,yy+187,title,INK,13)
        c.label(x+17,yy+215,sub.upper(),GRAY,10)
    return c

def scene6(t,u):
    c=Art()
    p=ease((u-.1)/1.4)
    for i in range(7):
        x=-70+i*205; xx=x+(610-x)*p
        c.line([(xx,-50),(xx+320,240)],mix(INK,VIOLET,.14+i*.04),2)
    c.rect(119,133,133,568,VIOLET)
    c.reveal(164,145,'BRAVADO',u,.26,127,PAPER)
    c.rect(164,337,164+923*ease((u-.73)/.55),343,LIME)
    c.reveal(166,390,'You built it, you shipped it,',u,.87,39,PAPER,'body')
    c.reveal(166,444,'now show your Bravado.',u,1.08,39,LIME,'body')
    if u>1.73:
        c.rect(166,542,540,605,VIOLET,r=5)
        c.text(190,556,'SHOW YOUR BRAVADO',21,PAPER)
        c.line([(503,573),(516,573),(509,566)],PAPER,2)
    c.label(166,635,'SITE OR GITHUB LINK  /  PRODUCT FILM WORKFLOW',GRAY,11)
    return c

SCENES=[scene0,scene1,scene2,scene3,scene4,scene5,scene6]
def frame(t):
    i=next((j for j in range(7) if t<CUTS[j+1]),6);u=t-CUTS[i]
    current=SCENES[i](t,u).im
    if i and u<.3:
        previous=SCENES[i-1](CUTS[i]-.001,CUTS[i]-CUTS[i-1]-.001).im
        edge=round(H*(1-ease(u/.3)))
        previous.paste(current.crop((0,edge,W,H)),(0,edge))
        ImageDraw.Draw(previous).rectangle((0,max(0,edge-5),W,edge),fill=VIOLET)
        return previous
    return current

def audio(path):
    sr=48000;n=sr*DURATION;mixdown=np.zeros((n,2),dtype=np.float32);rng=np.random.default_rng(619706)
    def put(at,sig,vol=.1,pan=0):
        k=round(at*sr);m=min(len(sig),n-k)
        if k<0 or m<=0:return
        mixdown[k:k+m,0]+=sig[:m]*vol*math.sqrt((1-pan)/2)
        mixdown[k:k+m,1]+=sig[:m]*vol*math.sqrt((1+pan)/2)
    def hit(at,vol=.16):
        z=np.arange(round(sr*.31))/sr
        sig=np.sin(2*np.pi*(71*z-38*z*z))*np.exp(-z*22)
        put(at,sig,vol)
    def tick(at,f=920,vol=.045,pan=0):
        z=np.arange(round(sr*.13))/sr
        put(at,(np.sin(2*np.pi*f*z)+.18*np.sin(4*np.pi*f*z))*np.exp(-z*32),vol,pan)
    def sweep(at,vol=.11):
        z=np.arange(round(sr*.34))/sr;noise=rng.normal(0,1,len(z))
        filtered=np.convolve(noise,np.ones(13)/13,'same')
        put(at,filtered*np.sin(np.pi*z/.34)**2,vol,-.35)
        put(at+.016,filtered*np.sin(np.pi*z/.34)**2,vol,.4)
    z=np.arange(n)/sr;fade=np.minimum(1,z/1.1)*np.minimum(1,(31-z)/.7)
    # Original D minor pulse. Sparse enough for the typography and effects to breathe.
    for freq,vol in [(73.416,.012),(110,.009),(146.832,.006),(174.614,.005),(220,.004)]:
        wavelet=np.sin(2*np.pi*freq*z+.12*np.sin(2*np.pi*.17*z))*vol*fade
        mixdown[:,0]+=wavelet;mixdown[:,1]+=np.roll(wavelet,round(sr*.004))
    for at in np.arange(.18,30,.5):
        hit(float(at),.048)
        tick(float(at+.25),1046,.023,.45)
    for at in CUTS[1:-1]:sweep(at-.16,.18);hit(at+.04,.18)
    for at in [.3,.72,1.38,4.4,4.75,5.1,9.05,9.36,9.65,12.3,12.66,13.0,24,24.3,24.6,27.45,28.13,28.34]:
        hit(at,.14);tick(at+.055,740,.065,-.3)
    for i in range(7):tick(18.05+i*.34,760+i*46,.09,(i-3)/5)
    for f in [293.665,349.228,440,587.33]:
        zz=np.arange(sr*2)/sr;put(27.72,np.sin(2*np.pi*f*zz)*np.exp(-zz*2.5),.036)
    peak=float(np.max(np.abs(mixdown)));mixdown*=min(1,.88/peak)
    with wave.open(str(path),'wb') as out:
        out.setnchannels(2);out.setsampwidth(2);out.setframerate(sr)
        out.writeframes((np.clip(mixdown,-1,1)*32767).astype('<i2').tobytes())

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default=str(ROOT/'output'/'bravado-pitch'))
    parser.add_argument('--stills',action='store_true')
    args=parser.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    review=out/'review';review.mkdir(exist_ok=True)
    times=[1.85,5.9,10.25,15.5,20.7,25.5,29.1]
    contact=Image.new('RGB',(1280,4*384),PAPER);d=ImageDraw.Draw(contact)
    for i,sec in enumerate(times):
        im=frame(sec);im.save(review/f'frame-{sec:.2f}.jpg',quality=88)
        thumb=im.resize((640,360));x=i%2*640;y=i//2*384
        contact.paste(thumb,(x,y));d.text((x+10,y+363),f'{sec:.2f} s',font=font(10,'mono'),fill=INK)
    contact.save(review/'storyboard.jpg',quality=90)
    if args.stills:return
    stem=out/'sound-design.wav';audio(stem)
    mp4=out/'bravado-product-pitch.mp4'
    cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-',
         '-i',str(stem),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','192k','-movflags','+faststart','-t','31',str(mp4)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(FPS*DURATION):
        proc.stdin.write(frame(i/FPS).tobytes())
        if i%150==0:print(f'Rendered {i}/{FPS*DURATION}',flush=True)
    proc.stdin.close()
    if proc.wait():raise RuntimeError('FFmpeg failed')
    print(mp4)
if __name__=='__main__':main()
