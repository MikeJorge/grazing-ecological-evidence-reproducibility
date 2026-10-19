"""Algorithm unit tests, not extra ecological scenarios or field validation."""
import copy, itertools, json, sys, unittest
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from reproduce import classify, interval, joint, load_inputs, reproduce

class Rules(unittest.TestCase):
    def setUp(self):
        self.d=json.loads((ROOT/'data/synthetic_inputs.json').read_text());self.p=json.loads((ROOT/'config/protocol.json').read_text())
    def test_sign_boundaries(self):
        for a,s in [(['-1','0'],'I'),(['0','0'],'A'),(['0','1'],'A'),(['-2','-1'],'V'),(['-0.00000000000000000001','-0.00000000000000000001'],'V')]:
            with self.subTest(a=a):self.assertEqual(classify(interval(a)),s)
    def test_unknown_not_zero(self):self.assertEqual(classify(None),'I')
    def test_all_profiles(self):
        for states in itertools.product('AVI',repeat=3):
            expected='V' if 'V' in states else 'A' if set(states)=={'A'} else 'I'
            self.assertEqual(joint(states),expected)
    def test_joint_rejects_invalid(self):
        for states in [[],['A','X'],['V',None]]:
            with self.assertRaises(ValueError):joint(states)
    def test_five_frozen_cases(self):
        ex=json.loads((ROOT/'expected/table1_expected.json').read_text())
        for r in reproduce(self.d,self.p):self.assertEqual({k:r[k] for k in ex[r['case']]},ex[r['case']])
    def test_missing_reason_retained_under_V(self):
        r=reproduce(self.d,self.p)[0];self.assertEqual(r['joint'],'V');self.assertIn('unavailable',r['indetermination_reasons']['K2'])
    def test_invalid_bounds_and_numbers(self):
        for a in [['2','1'],['NaN','2'],['1','Infinity'],['x','2'],[0,'2']]:
            d=copy.deepcopy(self.d);d['records'][0].update(lower=a[0],upper=a[1])
            with self.assertRaises(ValueError):reproduce(d,self.p)
    def test_conflicting_duplicate(self):
        r=copy.deepcopy(self.d['records'][0]);r['lower']='41';self.d['records'].append(r)
        with self.assertRaises(ValueError):reproduce(self.d,self.p)
    def test_identical_duplicate_no_weight(self):
        orig=reproduce(self.d,self.p);self.d['records'].append(copy.deepcopy(self.d['records'][0]));self.assertEqual(orig,reproduce(self.d,self.p))
    def test_negative_conversion_rejected(self):
        next(r for r in self.d['records'] if r['quantity_id']=='conversion')['lower']='-1'
        with self.assertRaises(ValueError):reproduce(self.d,self.p)
    def test_bad_protocol_ids(self):
        for ids in [[],['K1','K1','K3'],['K1','K2','K4']]:
            p=copy.deepcopy(self.p);p['criteria']=ids
            with self.assertRaises(ValueError):reproduce(self.d,p)
    def test_contradictory_unit_metadata(self):
        self.d['records'][0]['unit']='ha'
        with self.assertRaises(ValueError):reproduce(self.d,self.p)
    def test_valid_other_time_ineligible(self):
        r=self.d['records'][0];r.update(time_support=['3'],status='ineligible',missing_reason='observed at another time')
        z=reproduce(self.d,self.p)[0];self.assertEqual(z['profile'][0],'I');self.assertIn('another time',z['indetermination_reasons']['K1'])
    def test_unmarked_time_mismatch_rejected(self):
        self.d['records'][0]['time_support']=['3']
        with self.assertRaises(ValueError):reproduce(self.d,self.p)
    def test_missing_with_zero_not_allowed(self):
        r=next(r for r in self.d['records'] if r['status']=='missing');r['lower']='0';r['upper']='0'
        with self.assertRaises(ValueError):reproduce(self.d,self.p)
    def test_missing_reason_required(self):
        next(r for r in self.d['records'] if r['status']=='missing')['missing_reason']=''
        with self.assertRaises(ValueError):reproduce(self.d,self.p)
    def test_absent_record_not_silent_unknown(self):
        self.d['records'].pop()
        with self.assertRaises(ValueError):reproduce(self.d,self.p)
    def test_nonpositive_duration_rejected(self):
        self.p['duration_years']='0'
        with self.assertRaises(ValueError):reproduce(self.d,self.p)
    def test_duration_must_match_frozen_endpoints(self):
        self.p['duration_years']='10'
        with self.assertRaises(ValueError):reproduce(self.d,self.p)
    def test_orientation_conflict_rejected(self):
        self.p['orientations']['K1']='panel minus target'
        with self.assertRaises(ValueError):reproduce(self.d,self.p)
    def test_protocol_units_and_windows_frozen(self):
        for key in ['supports','quantities']:
            p=copy.deepcopy(self.p)
            if key=='supports':p[key]['stock']['unit']='ha'
            else:p[key]['sediment']['time_support']=['3','5']
            with self.assertRaises(ValueError):reproduce(self.d,p)
    def test_missing_top_level_and_protocol_fields(self):
        for key in ['baseline_filename','schema_version','coverage_claim']:
            d=copy.deepcopy(self.d);del d[key]
            with self.assertRaises(ValueError):reproduce(d,self.p)
        p=copy.deepcopy(self.p);del p['orientations']
        with self.assertRaises(ValueError):reproduce(self.d,p)
    def test_temporal_outputs_do_not_change_joint(self):
        before=reproduce(self.d,self.p)
        for r in self.d['records']:
            if r['quantity_id']=='baseline_stock' and r['status']=='eligible':r.update(lower='100',upper='101')
        after=reproduce(self.d,self.p)
        self.assertEqual([r['joint'] for r in before],[r['joint'] for r in after]);self.assertNotEqual(before[3]['change'],after[3]['change'])
    def test_temporal_unavailable_reasons_identify_actual_records(self):
        scenarios = [
            [('stock', 'missing', 'current stock not observed')],
            [('stock', 'ineligible', 'current stock uses another support')],
            [('baseline_stock', 'missing', 'baseline stock not observed')],
            [('baseline_stock', 'ineligible', 'baseline stock uses another support')],
            [('stock', 'missing', 'current stock not observed'),
             ('baseline_stock', 'ineligible', 'baseline stock uses another support')],
        ]
        for unavailable in scenarios:
            with self.subTest(unavailable=unavailable):
                data = copy.deepcopy(self.d)
                for quantity, status, reason in unavailable:
                    record = next(r for r in data['records']
                                  if r['scenario_id'] == 'D' and r['quantity_id'] == quantity)
                    record.update(status=status, missing_reason=reason)
                    if status == 'missing':
                        record.update(lower=None, upper=None)
                    else:
                        record['time_support'] = ['3']
                result = next(r for r in reproduce(data, self.p) if r['case'] == 'D')
                self.assertIsNone(result['change'])
                self.assertIsNone(result['rate'])
                self.assertEqual(result['temporal_missing_reason'],
                                 '; '.join(reason for _, _, reason in unavailable))
    def test_component_accounting(self):
        for q in range(1,6):
            for h in range(q+1):
                criteria={('K1',i) for i in range(q)}|{('K2',i) for i in range(q)}|{('K3','F')}
                quantities={(j,i) for i in range(q) for j in ['S','SR','E','ER']}|{('L','F')}|{('S0',i) for i in range(h)}
                self.assertEqual(len(criteria),2*q+1);self.assertEqual(len(quantities),4*q+1+h)
if __name__=='__main__':unittest.main(verbosity=2)
