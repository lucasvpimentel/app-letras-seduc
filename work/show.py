import json,re,html,sys
J=json.load(open('data/questoes.json',encoding='utf8')); g=json.load(open('data/gabarito.json'))['questoes']
pl=lambda h: html.unescape(re.sub(r'<br>',' / ',re.sub(r'</?[biu]>','',h)))
for i in range(int(sys.argv[1]),int(sys.argv[2])+1):
    q=J['questoes'][i-1]; print(f"## Q{i} [{g[str(i)]['letra'] or 'ANULADA'}]")
    if len(sys.argv)>3 and sys.argv[3]=='alts':
        print(' | '.join(f"{k}) {pl(v)}" for k,v in q['alternativas'].items())); continue
    print('\n'.join(pl(p) for p in q['enunciado']))
    print(' | '.join(f"{k}) {pl(v)}" for k,v in q['alternativas'].items()))
