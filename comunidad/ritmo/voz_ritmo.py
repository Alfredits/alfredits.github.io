"""Quita silencios >0,22 s (deja 0,1 s) y acelera a 1,1x. Uso: python voz_ritmo.py assets/voz.mp3 assets/voz-rapida.wav"""
import subprocess,re,sys
src,dst=sys.argv[1],sys.argv[2]
log=subprocess.run(['ffmpeg','-hide_banner','-i',src,'-af','silencedetect=noise=-38dB:d=0.22','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
K=.05;keep=[];a=0
for s,e in zip(st,en):
    if e>=dur-.05: break
    keep.append((a,s+K)); a=e-K
keep.append((a,dur))
sel='+'.join(f'between(t,{x:.3f},{y:.3f})' for x,y in keep)
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',src,'-af',f"aselect='{sel}',asetpts=N/SR/TB,atempo=1.1",dst],check=True)
