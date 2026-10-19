"""Exact arithmetic reconstruction for the frozen five-case demonstration.

This defensive implementation reproduces the five stipulated synthetic cases.
It verifies stated rule behavior; it neither estimates uncertainty nor validates ecology.
Run: python src/reproduce.py --out outputs
"""
import argparse, csv, json
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASELINE_SHA256='7fa29dbab06e9df4aa004e2e176b7b22dee818ea6fe005c51278ffa7a669f0ed'
def validate_protocol(protocol):
    """This release reconstructs the frozen protocol, not arbitrary new protocols."""
    schema=json.loads((ROOT/'schema/protocol.schema.json').read_text())
    if not isinstance(protocol,dict) or not set(schema['required']).issubset(protocol):
        raise ValueError('Missing protocol fields')
    for key,spec in schema['properties'].items():
        if 'const' in spec and protocol.get(key)!=spec['const']:
            raise ValueError('Frozen protocol conflict: '+key)
    for key in ['criticality','panel','duplicates','missingness','exact_zero']:
        if not isinstance(protocol[key],str) or not protocol[key].strip():
            raise ValueError('Missing protocol definition: '+key)
    quantities=protocol['quantities']
    t0=number(quantities['baseline_stock']['time_support'][0])
    t1=number(quantities['stock']['time_support'][0])
    if number(protocol['duration_years'])!=t1-t0 or t1<=t0:
        raise ValueError('Duration must equal the positive frozen endpoint difference')
def dump(path, obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def number(v):
    if not isinstance(v,str): raise ValueError('Numbers must be finite decimal strings')
    try: d=Decimal(v)
    except InvalidOperation as e: raise ValueError('Malformed number') from e
    if not d.is_finite(): raise ValueError('Nonfinite number')
    if len(d.as_tuple().digits)>28: raise ValueError('Unsupported precision')
    return d
def interval(a):
    if not isinstance(a,(list,tuple)) or len(a)!=2: raise ValueError('Interval needs two bounds')
    l,u=map(number,a)
    if l>u: raise ValueError('Reversed bounds')
    return l,u
def classify(a):
    if a is None: return 'I'
    l,u=a
    if not l.is_finite() or not u.is_finite() or l>u: raise ValueError('Invalid margin')
    return 'V' if u<0 else ('A' if l>=0 else 'I')
def joint(states):
    if not states or any(s not in ['A','V','I'] for s in states): raise ValueError('Invalid conclusion set')
    return 'V' if 'V' in states else ('A' if all(s=='A' for s in states) else 'I')
def difference(x,y): return x[0]-y[1],x[1]-y[0]
def strings(a):
    if a is None:return None
    def fmt(x): return '0' if x==0 else format(x.normalize(),'f')
    return [fmt(x) for x in a]
def load_inputs(data,protocol):
    validate_protocol(protocol)
    required_top={'schema_version','baseline_filename','baseline_sha256','synthetic','uncertainty_kind','coverage_claim','records'}
    if not isinstance(data,dict) or not required_top.issubset(data):raise ValueError('Missing input fields')
    if data['schema_version']!='1.0' or data['baseline_sha256']!=BASELINE_SHA256:raise ValueError('Unsupported schema/baseline')
    if data['baseline_filename']!='synthetic_source_reference.docx':raise ValueError('Conflicting baseline filename')
    if not isinstance(data['records'],list) or not data['records']:raise ValueError('Empty or malformed records')
    if protocol['criteria']!=['K1','K2','K3']: raise ValueError('Protocol requires the unique frozen K1,K2,K3 set')
    if data['synthetic'] is not True or data['uncertainty_kind']!='assumed_bounds' or data['coverage_claim'] is not None: raise ValueError('Unsupported inferential status')
    if data['baseline_sha256']!=protocol['baseline_sha256']:raise ValueError('Baseline identity conflict')
    if set(protocol['supports'])!=set(['stock','sediment','conversion']):raise ValueError('Malformed supports')
    found={}
    for r in data['records']:
        required={'scenario_id','stratum_id','quantity_id','support_id','unit','time_support','status','lower','upper','missing_reason','source_locator'}
        if not required.issubset(r):raise ValueError('Missing record field')
        if not isinstance(r['source_locator'],str) or not r['source_locator'].strip():raise ValueError('Missing source locator')
        if r['missing_reason'] is not None and not isinstance(r['missing_reason'],str):raise ValueError('Malformed missingness reason')
        if r['scenario_id'] not in list('ABCDE') or r['stratum_id']!='s1':raise ValueError('Unknown scenario/stratum')
        q=r['quantity_id']
        if q not in protocol['quantities']:raise ValueError('Unknown quantity')
        s=r['support_id']
        if s not in protocol['supports']:raise ValueError('Unknown support')
        support=protocol['supports'][s]
        if r['unit']!=support['unit']:raise ValueError('Contradictory unit/support metadata')
        ts=r['time_support']
        if not isinstance(ts,list) or len(ts) not in [1,2]:raise ValueError('Malformed time support')
        vals=list(map(number,ts))
        if len(vals)==2 and vals[0]>=vals[1]:raise ValueError('Invalid time order')
        if r['status'] not in ['eligible','missing','ineligible']:raise ValueError('Invalid status')
        if r['status']=='missing':
            if r['lower'] is not None or r['upper'] is not None or not r['missing_reason']:raise ValueError('Invalid missing record')
            a=None
        else:
            a=interval([r['lower'],r['upper']])
            if q=='conversion' and a[0]<0:raise ValueError('Negative gross conversion')
            if r['status']=='ineligible' and not r['missing_reason']:raise ValueError('Missing ineligibility reason')
        want=protocol['quantities'][q]
        eligibility=(s==want['support_id'] and ts==want['time_support'])
        if r['status']=='eligible' and not eligibility:raise ValueError('Mismatched evidence must be explicitly ineligible')
        key=(r['scenario_id'],q)
        if key in found:
            if found[key]['record']!=r:raise ValueError('Conflicting duplicate evidence')
            continue
        found[key]={'record':r,'interval':a if r['status']=='eligible' else None,'reason':r['missing_reason']}
    wanted={(c,q) for c in 'ABCDE' for q in protocol['quantities']}
    if set(found)!=wanted:raise ValueError('Incomplete/extra evidence inventory; missingness must be explicit')
    return found
def reproduce(data,protocol):
    records=load_inputs(data,protocol);out=[]
    T=number(protocol['duration_years'])
    if T<=0:raise ValueError('Nonpositive duration')
    for c in 'ABCDE':
        def get(q):return records[(c,q)]['interval']
        margins={};reasons={}
        for k,qs in [('K1',['stock','panel_stock']),('K2',['panel_sediment','sediment']),('K3',['conversion'])]:
            if any(get(q) is None for q in qs):
                margins[k]=None;reasons[k]='; '.join(q+': '+records[(c,q)]['reason'] for q in qs if get(q) is None)
            else:
                margins[k]=(-get(qs[0])[1],-get(qs[0])[0]) if k=='K3' else difference(get(qs[0]),get(qs[1]))
                reasons[k]='eligible interval spans the decision boundary' if classify(margins[k])=='I' else None
        profile=[classify(margins[k]) for k in protocol['criteria']]
        change=difference(get('stock'),get('baseline_stock')) if get('stock') is not None and get('baseline_stock') is not None else None
        rate=tuple(v/T for v in change) if change is not None else None
        temporal_reason='; '.join(records[(c,q)]['reason'] for q in ['stock','baseline_stock'] if get(q) is None) or None
        out.append({'case':c,'margins':{k:strings(v) for k,v in margins.items()},'profile':profile,'joint':joint(profile),'indetermination_reasons':reasons,'change':strings(change),'rate':strings(rate),'temporal_missing_reason':temporal_reason,'units':{'K1':'Mg C ha^-1','K2':'Mg ha^-1 over (4,5]','K3':'ha over [0,5]','change':'Mg C ha^-1','rate':'Mg C ha^-1 yr^-1'}})
    return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='outputs');args=ap.parse_args()
    data=json.loads((ROOT/'data/synthetic_inputs.json').read_text());protocol=json.loads((ROOT/'config/protocol.json').read_text())
    with localcontext() as ctx:
        ctx.prec=50;result=reproduce(data,protocol)
    expected=json.loads((ROOT/'expected/table1_expected.json').read_text())
    for row in result:
        actual={k:row[k] for k in ['case','margins','profile','joint','change','rate']}
        assert actual==expected[row['case']],(actual,expected[row['case']])
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    dump(out/'results.json',{'synthetic':True,'uncertainty_kind':'assumed_bounds','coverage_claim':None,'cases':result})
    with (out/'table1.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['Case','K1','K2','K3','Profile','D','Delta S','r'])
        for r in result:
            def show(x):return '—' if x is None else '['+', '.join(x)+']'
            w.writerow([r['case'],show(r['margins']['K1']),'Unknown' if r['margins']['K2'] is None else show(r['margins']['K2']),show(r['margins']['K3']),'/'.join(r['profile']),r['joint'],show(r['change']),show(r['rate'])])
    print('Five synthetic cases reproduced; no coverage or ecological validation implied.')
if __name__=='__main__':main()
