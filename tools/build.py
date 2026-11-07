import re,os,shutil,sys,datetime
S='/tmp/claude-0/-home-claude/83eefa74-e018-5b70-800e-20cd3ed4aff7/scratchpad/artifact-files/'
OUT='/home/claude/travel-pages/'
L='/tmp/lib/node_modules/'
LIBS={
 'd3':open(L+'d3/dist/d3.min.js',encoding='utf8').read(),
 'topojson-client':open(L+'topojson-client/dist/topojson-client.min.js',encoding='utf8').read(),
 'three.min':open(L+'three/build/three.min.js',encoding='utf8').read(),
 'OrbitControls':open(L+'three/examples/js/controls/OrbitControls.js',encoding='utf8').read(),
}
P=[
('6be4b0a7-d82f-4b64-b40e-2c4bc2a115d3','archipelago.html','超民の旅の群島','總覽','EKjzzck1Rk5wkWRw8wui8S'),
('5aa2207e-584e-48da-b3ed-771044bc1516','jr-map.html','日本 JR 乘車地圖','日本','CC8B1DxnM9D9rJQkkDzafF'),
('235d6c6a-62d4-4c3c-a62c-086b8af8f40a','stamp-japan.html','日本スタンプ旅','スタンプ','5NHdeFcuzpUgua9n44PevM'),
('97b252d7-adc6-4771-a1e1-3cb08c102932','stamp-china.html','中国スタンプ旅','スタンプ','KjTvJJRnjh8a7Sd2pA3T1B'),
('8cbe1003-bfe2-4bda-9ee3-c7f19b18c24d','stamp-australia.html','オーストラリアスタンプ旅','スタンプ','JP1ZE2CEBAfTZPYWnELFji'),
('d31d00ea-9319-41d6-8d57-305cb4d01a51','stamp-uk.html','イギリススタンプ旅','スタンプ','T51gqrYAHw42mATvSTEAVn'),
('400305e4-990e-4405-bad3-aa8059b0fee1','stamp-italy.html','イタリアスタンプ旅','スタンプ','8uTaFUqxP6cvzWtcrHy82C'),
('0117170b-3a0c-47d6-8123-cd7efe4faf03','stamp-hongkong.html','香港スタンプ旅','スタンプ','18osN1aSLGTCpmCLoKsNhG'),
('db6be2ec-5fe3-42c6-b20a-d50927b0273a','stamp-hawaii.html','ハワイスタンプ旅','スタンプ','U6WtwRcSDwJc6o9XVLJ177'),
('62597aa4-2c08-476a-bfdf-8f7fa39fcad6','stamp-marshall.html','マーシャル諸島スタンプ旅','スタンプ','D9PVtqFTCyk7x9ebnXmEPf'),
('2c62d731-9a13-4322-a61c-24c4346080c3','stamp-singapore.html','シンガポールスタンプ旅','スタンプ','6Uu2pkCi4HvQ73W7MAk5ia'),
('84733fde-6dd4-4caa-b921-90cdb7d9da75','stamp-vietnam.html','ベトナムスタンプ旅','スタンプ','HMcx9pZJeH2D95ak37oAKE'),
('f9fc0f34-fa2e-4903-8c47-5e4e5249ce48','stamp-switzerland.html','スイススタンプ旅','スタンプ','XsQsXTcm9DLHX5MZ2kTFNo'),
('85b2040a-aac4-45ca-bbf5-68d8ca828819','stamp-thailand.html','タイスタンプ旅','スタンプ','HWYCcyQ2FS1eFq69iDVnC8'),
('e8d39655-0706-43d7-a003-d007ba438bbe','stamp-czech.html','チェコスタンプ旅','スタンプ','VkXP4z8JQRbsrCwFC4UBRX'),
('935bf3fb-2a9e-4039-85f1-7f9fb67bf532','train-trip/index.html','超民の列車の旅','列車','KCQAYmS6UxYgty5Zs9q75s'),
('694c21dc-128e-4b94-8ca5-86f2c960de16','hero-train/index.html','鉄道勇者ちょうみんの冒険','列車','E19ebmqXqd2ekRsqBez8f7'),
]
idmap={p[4]:p[1] for p in P}
def rel(frm,to): return os.path.relpath(to,os.path.dirname(frm) or '.')
def inline(m):
    u=m.group(1)
    for k,v in LIBS.items():
        if '/'+k in u:
            return '<script>'+v.replace('</script','<\\/script')+'</script>'
    print('UNKNOWN SCRIPT',u); return m.group(0)
for slug,out,title,grp,aid in P:
    h=open(S+slug+'/index.html',encoding='utf8').read()
    h=re.sub(r'<script[^>]*src="(https://[^"]+)"[^>]*></script>',inline,h)
    h=re.sub(r'<link[^>]*(?:fonts\.googleapis|fonts\.gstatic)[^>]*>\s*','',h)
    for i,f in idmap.items():
        h=h.replace('https://claude.ai/artifact/'+i,rel(out,f))
    ext=sorted({u for u in re.findall(r'https?://[^\s"\'<>)]+',h) if any(k in u for k in('claude.ai','googleapis','cdn','gstatic'))})
    if ext: print(out,'EXTERNAL:',ext[:5])
    os.makedirs(os.path.dirname(OUT+out),exist_ok=True)
    open(OUT+out,'w',encoding='utf8').write(h)
    ph=S+slug+'/photos'
    if os.path.isdir(ph):
        d=os.path.dirname(OUT+out)+'/photos'
        shutil.rmtree(d,ignore_errors=True); shutil.copytree(ph,d)
    print('ok',out,len(h))
groups={}
for slug,out,title,grp,aid in P: groups.setdefault(grp,[]).append((out,title))
cards=''
for g in ['總覽','日本','スタンプ','列車']:
    cards+=f'<h2>{g}</h2><ul>'+''.join(f'<li><a href="{o}">{t}</a></li>' for o,t in groups[g])+'</ul>'
idx=f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>超民の旅 目錄</title>
<style>body{{font-family:"Noto Sans TC","Noto Sans JP",sans-serif;max-width:640px;margin:0 auto;padding:24px 16px;background:#faf7f0;color:#222}}h1{{font-size:1.5rem}}h2{{font-size:1.05rem;border-bottom:2px solid #d9cfb8;padding-bottom:4px;margin-top:28px}}ul{{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px}}li a{{display:block;padding:12px 14px;background:#fff;border:1px solid #e3dac4;border-radius:10px;text-decoration:none;color:#222}}li a:hover{{background:#fff3d6}}small{{color:#888}}@media(prefers-color-scheme:dark){{body{{background:#1b1a17;color:#eee}}li a{{background:#2a2823;border-color:#3d3a31;color:#eee}}h2{{border-color:#444}}}}</style></head><body>
<h1>超民の旅 目錄</h1><small>離線版（更新：{datetime.date.today()}）</small>{cards}</body></html>'''
open(OUT+'index.html','w',encoding='utf8').write(idx)
