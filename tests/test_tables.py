"""Behavioral regression suite; usable against a complete RSI candidate tree."""
from __future__ import annotations
import argparse
import copy
import importlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

parser=argparse.ArgumentParser(add_help=False)
parser.add_argument('--candidate',type=Path)
args,remaining=parser.parse_known_args()
CANDIDATE=(args.candidate or Path(__file__).resolve().parents[1]).resolve()
sys.path.insert(0,str(CANDIDATE/'scripts'))
from tablelib import check_spec, compare, decimal, delta, generate, rankings, read_json, retrieve, sha256, static_check, strip_comments, write_json
from index_cases import build_index
from compile_table import compile_source
import rsi
import export_public
import learning

def fixture(name='ties-missing'):
    return read_json(CANDIDATE/'assets'/'templates'/(name+'.json'))

class NumericalTests(unittest.TestCase):
    def test_json_duplicate_values_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'duplicate.json'
            p.write_text('{"values":{"auc":"91.00","auc":"89.00"}}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Duplicate JSON key'):
                read_json(p)

    def test_json_nonstandard_numbers_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'nonstandard.json'
            for token in ('NaN','Infinity','-Infinity'):
                p.write_text('{"value":'+token+'}',encoding='utf-8')
                with self.subTest(token=token),self.assertRaises(ValueError): read_json(p)

    def test_ties_and_missing(self):
        marks=rankings(fixture())
        self.assertEqual(marks['A','auc'],'best'); self.assertEqual(marks['B','auc'],'best')
        self.assertEqual(marks['C','auc'],'second'); self.assertNotIn(('D','auc'),marks)
        self.assertEqual(marks['B','error'],'best'); self.assertEqual(marks['D','error'],'second')
        self.assertNotIn(('A','params'),marks)

    def test_groups_and_exclusion(self):
        s=fixture(); s['rows'][0]['eligible']=False; s['rows'][2]['group']='other'
        marks=rankings(s)
        self.assertNotIn(('A','auc'),marks); self.assertEqual(marks['C','auc'],'best')

    def test_zero_is_ranked(self):
        s=fixture(); s['rows'][0]['values']['error']='0.0'
        self.assertEqual(rankings(s)['A','error'],'best')

    def test_exact_precision(self):
        s=fixture('benchmark'); text=generate(s)
        self.assertIn('81.20',text)
        altered=copy.deepcopy(s); altered['rows'][0]['values']['auc']='81.2'
        self.assertTrue(compare(s,altered))

    def test_swap_caught(self):
        s=fixture('benchmark'); t=copy.deepcopy(s)
        t['rows'][0]['values'],t['rows'][1]['values']=t['rows'][1]['values'],t['rows'][0]['values']
        self.assertEqual(len(compare(s,t)),2)

    def test_reordering_not_data_change(self):
        s=fixture('benchmark'); t=copy.deepcopy(s); t['rows'].reverse()
        self.assertEqual(compare(s,t),[])

    def test_caption_and_row_header_changes_caught(self):
        s=fixture('benchmark'); t=copy.deepcopy(s)
        t['caption']='A different scientific claim'; t['row_header']='Dataset'
        self.assertEqual(set(compare(s,t)),{'spec.caption: changed','spec.row_header: changed'})

    def test_layout_changes_are_optional_comparison(self):
        s=fixture('benchmark'); t=copy.deepcopy(s)
        t.update(float='table*',label='tab:other',alignment='center')
        self.assertEqual(compare(s,t),[])
        self.assertEqual(set(compare(s,t,include_presentation=True)),{'spec.float: changed','spec.label: changed'})

    def test_unit_and_group_change_caught(self):
        s=fixture('benchmark'); t=copy.deepcopy(s); t['columns'][0]['unit']='fraction'; t['rows'][0]['group']='changed'
        self.assertEqual(len(compare(s,t)),2)

    def test_directions_explicit(self):
        s=fixture(); del s['columns'][0]['direction']
        with self.assertRaises(ValueError): check_spec(s)

    def test_nonfinite_and_float_rejected(self):
        for v in ('NaN','Infinity','-Infinity','85.2%',85.2):
            with self.subTest(v=v),self.assertRaises(ValueError): decimal(v)

    def test_schema_rejects_duplicates_and_missing(self):
        for bad in ('duplicate','missing'):
            s=fixture()
            if bad=='duplicate': s['rows'][1]['id']=s['rows'][0]['id']
            else: del s['rows'][0]['values']['auc']
            with self.assertRaises(ValueError): check_spec(s)

    def test_uncertainty_opt_in(self):
        s=fixture('uncertainty'); self.assertEqual(rankings(s)['B','auc'],'best')
        del s['columns'][0]['rank_on']
        with self.assertRaises(ValueError): check_spec(s)

    def test_invalid_ci(self):
        s=fixture('uncertainty'); s['rows'][0]['values']['f1']['ci']=['80','90']
        with self.assertRaises(ValueError): check_spec(s)

    def test_delta_semantics(self):
        self.assertEqual(delta('55','50','percentage_points'),5)
        self.assertEqual(delta('55','50','relative_percent'),10)
        self.assertEqual(delta('49','50','absolute'),-1)
        with self.assertRaises(ValueError): delta('1','0','relative_percent')

    def test_long_precision_delta(self):
        self.assertEqual(str(delta('100000000000000000000000000000.01','100000000000000000000000000000.00','absolute')),'0.01')

    def test_escape_data_not_code(self):
        s=fixture('benchmark'); s['rows'][0]['label']=r'A&B_50% \input{secret}'
        text=generate(s)
        self.assertIn(r'A\&B\_50\%',text); self.assertNotIn(r'\input{secret}',text)

    def test_greater_and_less_are_text_glyphs(self):
        s=fixture('benchmark'); s['row_header']='A -> B < C'
        self.assertIn(r'A -\textgreater{} B \textless{} C',generate(s))

    def test_decimal_scientific_token_is_not_math_wrapped(self):
        self.assertIn('Exponent & 1.2e-3',generate(fixture('decimal')))

    def test_every_authored_contract(self):
        for path in sorted((CANDIDATE/'assets'/'templates').glob('*.json')):
            with self.subTest(path=path.name):
                s=read_json(path); check_spec(s); self.assertEqual(compare(s,s),[])
                self.assertFalse(static_check(generate(s))['errors'])

class StaticTests(unittest.TestCase):
    def test_booktabs_spacing_is_not_a_data_row(self):
        result=static_check(r'\begin{tabular}{lcc}a&b&c\\\addlinespace[2pt]\bottomrule\end{tabular}')
        self.assertFalse(result['errors']); self.assertIn('booktabs',result['inferred_packages'])

    def test_decimal_dependency_is_inferred(self):
        self.assertIn('siunitx',static_check(r'\begin{tabular}{SS}1&2\\\end{tabular}')['inferred_packages'])
    def test_rule_range_outside_columns(self):
        self.assertTrue(static_check(r'\begin{tabular}{lcc}\cmidrule(lr){2-5}a&b&c\\\end{tabular}')['errors'])
    def test_valid_multicolumn(self):
        self.assertFalse(static_check(r'\begin{tabular}{lcc}\multicolumn{2}{c}{A} & B \\ a&1&2\\\end{tabular}')['errors'])

    def test_bad_span(self):
        self.assertTrue(static_check(r'\begin{tabular}{lc}\multicolumn{3}{c}{A}\\\end{tabular}')['errors'])

    def test_missing_cell(self):
        self.assertTrue(static_check(r'\begin{tabular}{lcc}A&1\\\end{tabular}')['errors'])

    def test_nested_and_custom_unknown(self):
        result=static_check(r'\begin{tabular}{p{2cm}c}A&B\\\end{tabular}')
        self.assertEqual(result['status'],'needs_review')

    def test_comment_and_escaped_percent(self):
        self.assertEqual(strip_comments('x \\% y % ignored'),'x \\% y ')
        self.assertFalse(static_check('% {broken\n'+r'\begin{tabular}{lc}A&1\\\end{tabular}')['errors'])

    def test_unbalanced_and_duplicate(self):
        self.assertTrue(static_check(r'\begin{table}{') ['errors'])
        self.assertTrue(static_check(r'\label{a}\label{a}')['errors'])

class LearningTests(unittest.TestCase):
    def test_case_capture_preserves_bytes_and_stays_pending(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); source=p/'table.tex'; raw=b'71.00 \\pm 0.20'; source.write_bytes(raw)
            folder=learning.record(p/'state',kind='case',reason='Actual test fixture',sources=[source],case_id='test-case',columns=3)
            self.assertEqual(source.read_bytes(),raw); self.assertEqual((folder/'table.tex').read_bytes(),raw)
            meta=read_json(folder/'case.json'); self.assertFalse(meta['verified']); self.assertEqual(meta['status'],'pending')
            self.assertEqual(meta['sources'][0]['sha256'],sha256(source))

    def test_feedback_is_separate_from_case_library(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=learning.record(Path(tmp),kind='feedback',reason='Specific regression observation',sources=[],case_id='test-feedback')
            self.assertTrue((folder/'record.json').exists()); self.assertFalse((folder/'case.json').exists())

    def test_existing_learning_record_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            args=dict(kind='feedback',reason='Observed issue',sources=[],case_id='same-id')
            learning.record(Path(tmp),**args)
            with self.assertRaises(FileExistsError): learning.record(Path(tmp),**args)

    def test_learning_cannot_mutate_stable_tree(self):
        with self.assertRaisesRegex(ValueError,'outside'):
            learning.record(learning.ROOT/'history',kind='feedback',reason='test',sources=[])

    def test_empty_case_and_colliding_names_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); source=p/'table.tex'; source.write_text('test')
            with self.assertRaises(ValueError): learning.record(p/'state',kind='case',reason='test',sources=[])
            with self.assertRaises(ValueError): learning.record(p/'state',kind='case',reason='test',sources=[source,source])

class CaseTests(unittest.TestCase):
    def test_public_export_omits_environment_files_and_hidden_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp); skill=base/'paper-latex-table-skill'; scripts=skill/'scripts'; scripts.mkdir(parents=True)
            (skill/'SKILL.md').write_text('synthetic test skill',encoding='utf-8')
            for name in ('README.md','LICENSE','.gitignore'): (base/name).write_text('synthetic test notice',encoding='utf-8')
            (scripts/'helper.py').write_text('print(1)',encoding='utf-8')
            (scripts/'.env').write_text('SYNTHETIC_TEST_ONLY=not-a-secret',encoding='utf-8')
            (scripts/'debug.log').write_text('synthetic local log',encoding='utf-8')
            (scripts/'.private').mkdir(); (scripts/'.private'/'local.py').write_text('private fixture',encoding='utf-8')
            (skill/'README.md').write_text('![Preview](docs/images/preview.png)',encoding='utf-8')
            (skill/'docs'/'images').mkdir(parents=True)
            (skill/'docs'/'images'/'preview.png').write_bytes(b'synthetic-test-image')
            archive=base/'release.zip'
            with patch.object(export_public,'ROOT',skill): export_public.export(archive)
            import zipfile
            with zipfile.ZipFile(archive) as z:
                self.assertIn('paper-latex-table-skill/scripts/helper.py',z.namelist())
                self.assertIn('paper-latex-table-skill/README.md',z.namelist())
                self.assertEqual(z.read('paper-latex-table-skill/docs/images/preview.png'),b'synthetic-test-image')
                self.assertFalse(any(name.endswith(('.env','.log')) or '/.private/' in name for name in z.namelist()))

    def test_retrieve_structure_and_ties(self):
        cases=[{'case_id':'b','columns':9,'table_type':'ablation','features':['grouped_headers']},{'case_id':'a','columns':9,'table_type':'ablation','features':['grouped_headers']},{'case_id':'keyword','columns':4,'table_type':'resource','features':[]}]
        result=retrieve(cases,columns=9,table_type='ablation',features=['grouped_headers'])
        self.assertEqual([x['case']['case_id'] for x in result],['a','b','keyword'])

    def test_cases_are_hash_verified(self):
        self.assertGreaterEqual(len(build_index(CANDIDATE/'assets'/'cases')),8)

    def test_tamper_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); (p/'table.tex').write_text('a'); write_json(p/'case.json',{'case_id':'test','sources':[{'path':'table.tex','sha256':sha256(p/'table.tex')}]})
            (p/'table.tex').write_text('b')
            with self.assertRaises(ValueError): build_index(p)

class CompilerTests(unittest.TestCase):
    def test_file_line_error_rejects_zero_exit_with_pdf(self):
        with tempfile.TemporaryDirectory() as tmp,patch('compile_table.shutil.which',return_value='pdflatex'):
            p=Path(tmp); source=p/'x.tex'; source.write_text('x')
            def fake(*a,**kw):
                (p/'out'/'table-build.pdf').write_bytes(b'%PDF-test')
                (p/'out'/'table-build.log').write_text('./table-build.tex:12: Undefined control sequence.')
                return type('R',(),{'returncode':0,'stdout':b'','stderr':b''})()
            with patch('compile_table.subprocess.run',side_effect=fake):
                self.assertEqual(compile_source(source,p/'out')['status'],'failed')

    def test_no_engine_is_unavailable(self):
        with tempfile.TemporaryDirectory() as tmp,patch('compile_table.shutil.which',return_value=None):
            result=compile_source(Path(tmp)/'x.tex',Path(tmp)/'out')
            self.assertEqual(result['status'],'unavailable')

    def test_stale_output_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError): compile_source(Path(tmp)/'x',Path(tmp))

    def test_pdf_does_not_override_failure(self):
        with tempfile.TemporaryDirectory() as tmp,patch('compile_table.shutil.which',return_value='pdflatex'):
            p=Path(tmp); source=p/'x.tex'; source.write_text(r'\begin{tabular}{l}A\\\end{tabular}')
            def fail(*a,**kw):
                (p/'out'/'table-build.pdf').write_bytes(b'not really a PDF')
                (p/'out'/'table-build.log').write_text('! Undefined control sequence')
                return type('R',(),{'returncode':1,'stdout':b'failed','stderr':b''})()
            with patch('compile_table.subprocess.run',side_effect=fail):
                self.assertEqual(compile_source(source,p/'out')['status'],'failed')

    def test_timeout(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp,patch('compile_table.shutil.which',return_value='pdflatex'),patch('compile_table.subprocess.run',side_effect=subprocess.TimeoutExpired('tex',1)):
            p=Path(tmp); source=p/'x.tex'; source.write_text('x')
            self.assertEqual(compile_source(source,p/'out')['status'],'timeout')

class RSITests(unittest.TestCase):
    def make_evidence(self, p):
        candidate=p/'candidate'; candidate.mkdir(); (candidate/'change.py').write_text('original')
        digest=rsi.tree_hash(candidate); baseline=rsi.tree_hash(rsi.ROOT)
        write_json(p/'proposal.json',{'candidate':str(candidate),'candidate_hash':digest,'baseline_hash':baseline})
        (p/'tests.log').write_text('Synthetic regression fixture, not a real test run')
        write_json(p/'evaluation.json',{'status':'passed','returncode':0,'candidate_hash':digest,'baseline_hash':baseline,'tests_sha256':sha256(p/'tests.log'),'harness_sha256':sha256(rsi.ROOT/'tests'/'test_tables.py')})
        (p/'artifact.txt').write_text('Synthetic visual attestation fixture, not an inspected PDF')
        write_json(p/'visual.json',{'candidate_hash':digest,'status':'passed','reviewer':'unit-test-only','artifacts':[{'path':'artifact.txt','sha256':sha256(p/'artifact.txt')}]})
        return p/'visual.json'

    def test_acceptance_records_only_no_stable_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); visual=self.make_evidence(p); before=rsi.tree_hash(rsi.ROOT)
            record=rsi.accept(p,'unit-test-only','Test attestation only; no promotion authorized',visual)
            self.assertEqual(record['status'],'accepted_for_manual_integration')
            self.assertEqual(rsi.tree_hash(rsi.ROOT),before)
            with self.assertRaises(ValueError): rsi.accept(p,'test','test',visual)

    def test_changed_log_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); visual=self.make_evidence(p); (p/'tests.log').write_text('tampered')
            with self.assertRaises(ValueError): rsi.accept(p,'test','test',visual)

    def test_changed_artifact_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); visual=self.make_evidence(p); (p/'artifact.txt').write_text('tampered')
            with self.assertRaises(ValueError): rsi.accept(p,'test','test',visual)

    def test_unbound_visual_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); visual=self.make_evidence(p); v=read_json(visual); v['candidate_hash']='wrong'; write_json(visual,v)
            with self.assertRaises(ValueError): rsi.accept(p,'test','test',visual)

    def test_hash_changes_with_script_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); (p/'x.py').write_text('one'); before=rsi.tree_hash(p); (p/'x.py').write_text('two')
            self.assertNotEqual(before,rsi.tree_hash(p))

    def test_failed_and_stale_evidence_cannot_accept(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); candidate=p/'candidate'; candidate.mkdir(); (candidate/'x').write_text('a')
            digest=rsi.tree_hash(candidate)
            write_json(p/'proposal.json',{'candidate':str(candidate),'candidate_hash':digest,'baseline_hash':rsi.tree_hash(rsi.ROOT)})
            write_json(p/'evaluation.json',{'status':'failed','returncode':1})
            with self.assertRaises(ValueError): rsi.accept(p,'reviewer','approve',p/'visual.json')
            write_json(p/'evaluation.json',{'status':'passed','returncode':0,'candidate_hash':digest})
            (candidate/'x').write_text('changed')
            with self.assertRaises(ValueError): rsi.accept(p,'reviewer','approve',p/'visual.json')

    def test_state_cannot_be_in_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            with self.assertRaises(ValueError): rsi.propose(p,p/'state','fix','case')

    def test_state_cannot_be_in_stable_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError,'stable skill'):
                rsi.propose(Path(tmp),rsi.ROOT/'rsi-history','fix','case')

if __name__=='__main__':
    unittest.main(argv=[sys.argv[0]]+remaining,verbosity=2)
