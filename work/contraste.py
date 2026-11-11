# Calcula contraste WCAG para os pares de cores usados no tema escuro e no claro.
def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def cr(a,b):
    la,lb=sorted([lum(a),lum(b)],reverse=True); return (la+0.05)/(lb+0.05)
T={
 'escuro':dict(bg='#0e141b',card='#16202a',card2='#1c2833',line='#6f87a1',text='#eaf0f6',muted='#b4c1ce',accent='#ffc857',on_accent='#1a1300',ok='#6ee7a8',ok_bg='#0f2a1e',bad='#ff9a9a',bad_bg='#33171a',warn='#ffd27a',warn_bg='#2d2410',focus='#8fd0ff'),
 'claro':dict(bg='#f4f1e9',card='#ffffff',card2='#f0ece1',line='#7d7767',text='#1b2430',muted='#475262',accent='#1f4fbf',on_accent='#ffffff',ok='#0b6b3a',ok_bg='#e3f4ea',bad='#a21c1c',bad_bg='#fbe7e7',warn='#7a4a00',warn_bg='#fff1d6',focus='#0b57d0'),
}
pares=[('text','bg',4.5),('text','card',4.5),('text','card2',4.5),('muted','card',4.5),('muted','bg',4.5),('muted','card2',4.5),('on_accent','accent',4.5),
       ('ok','ok_bg',4.5),('ok','card',4.5),('bad','bad_bg',4.5),('bad','card',4.5),('text','ok_bg',4.5),('text','bad_bg',4.5),('text','warn_bg',4.5),
       ('line','card',3),('line','bg',3),('line','card2',3),('accent','card',3),('accent','bg',3),('focus','bg',3),('focus','card',3),('ok','bg',3),('bad','bg',3),('bad','card2',4.5),('ok','card2',4.5)]
falhas=0
for nome,c in T.items():
    for a,b,min_ in pares:
        v=cr(c[a],c[b]); ok=v>=min_
        if not ok: falhas+=1
        print(f"{nome:6} {a:9} on {b:8} {v:5.2f} (min {min_}) {'OK' if ok else 'FALHA'}")
print('falhas',falhas)
