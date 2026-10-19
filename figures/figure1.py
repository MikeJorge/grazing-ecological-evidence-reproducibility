"""Deterministic vector drawing; all geometry/text is supplied by JSON.

No source bitmap, generative image service, manual drawing, or output retouching.
Optional color-vision previews apply the declared matrix to vector colors before export.
"""
import argparse, datetime, hashlib, json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib import colors, font_manager
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
def rgb_transform(c,mode,config):
    rgb=np.array(colors.to_rgb(c))
    if mode=='normal':return rgb
    lin=np.where(rgb<=0.04045,rgb/12.92,((rgb+0.055)/1.055)**2.4)
    if mode=='grayscale':lin=np.repeat(np.dot(lin,[.2126,.7152,.0722]),3)
    else:lin=np.array(config['color_vision_matrices'][mode])@lin
    lin=np.clip(lin,0,1)
    return np.where(lin<=.0031308,12.92*lin,1.055*lin**(1/2.4)-.055)
def render(config,out,stem,mode='normal'):
    plt.rcParams.update({'font.family':config['font_family'],'font.size':config['font_size_pt'],'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','svg.hashsalt':'EI-Figure1-v0.1.0','path.simplify':False,'text.usetex':False})
    fig=plt.figure(figsize=(config['width_inches'],config['height_inches']),facecolor='white');ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,100),ylim=(0,100));ax.axis('off')
    t=lambda c:rgb_transform(c,mode,config)
    extents=[]
    for b in config['boxes']:
        x,y,w,h=b['rect'];p=Rectangle((x,y),w,h,facecolor=t(b['fill']),edgecolor=t(b['edge']),linewidth=.9);ax.add_patch(p)
        tx=ax.text(x+w/2,y+h/2,b['text'],ha='center',va='center',fontsize=b.get('font_size_pt',config['font_size_pt']),color=t(config['text_color']),linespacing=1.2)
        extents.append((b['id'],p,tx))
    for a in config['arrows']:
        ax.add_patch(FancyArrowPatch(a['from'],a['to'],arrowstyle='-|>',mutation_scale=9,linewidth=.8,color=t(config['arrow_color'])))
    for b in config.get('labels',[]):ax.text(*b['position'],b['text'],ha='center',va='center',fontsize=config['font_size_pt'],color=t(config['text_color']))
    fig.canvas.draw();renderer=fig.canvas.get_renderer();fit=[]
    for id,p,tx in extents:
        a=p.get_window_extent(renderer);b=tx.get_window_extent(renderer)
        fit.append({'box':id,'fits':bool(a.contains(b.x0,b.y0) and a.contains(b.x1,b.y1)),'box_px':list(a.bounds),'text_px':list(b.bounds)})
    if not all(r['fits'] for r in fit):raise ValueError('Text outside box: '+str([r['box'] for r in fit if not r['fits']]))
    out.mkdir(parents=True,exist_ok=True)
    fixed=datetime.datetime(2000,1,1,tzinfo=datetime.timezone.utc)
    # Fixed date is only deterministic file metadata, never an observation date.
    fig.savefig(out/(stem+'.pdf'),metadata={'Creator':'figure1.py','Producer':'Matplotlib','CreationDate':fixed,'ModDate':fixed})
    fig.savefig(out/(stem+'.svg'),metadata={'Creator':'figure1.py','Date':'2000-01-01','Title':'Conceptual information flow'})
    fig.savefig(out/(stem+'.png'),dpi=config['preview_dpi'],metadata={'Software':'figure1.py'})
    plt.close(fig)
    return fit
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--config',default='config/figure1.json');ap.add_argument('--out',default='outputs');ap.add_argument('--stem',default='Figure_1');ap.add_argument('--accessibility',action='store_true');args=ap.parse_args()
    config=json.loads((ROOT/args.config).read_text());out=Path(args.out)
    fit=render(config,out,args.stem)
    if args.accessibility:
        for m in ['grayscale','protanopia','deuteranopia','tritanopia']:render(config,out,args.stem+'_'+m,m)
    font=Path(font_manager.findfont(config['font_family'],fallback_to_default=False))
    (out/(args.stem+'_layout_checks.json')).write_text(json.dumps({'box_text_fit':fit,'font_file':str(font),'font_sha256':hashlib.sha256(font.read_bytes()).hexdigest(),'minimum_label_pt_at_configured_width':min([b.get('font_size_pt',config['font_size_pt']) for b in config['boxes']]),'configured_width_inches':config['width_inches'],'image_generation':'Python vector primitives only'},indent=2)+'\n')
    print('Rendered',args.stem,'with',len(fit),'contained text boxes')
if __name__=='__main__':main()
