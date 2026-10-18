#!/usr/bin/env python3
"""Validate a round record and render an offline research canvas; stdlib only."""
import argparse
import datetime
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def validate_schema(value, schema, root, path='$'):
    if '$ref' in schema:
        target = root
        for part in schema['$ref'].removeprefix('#/').split('/'):
            target = target[part]
        return validate_schema(value, target, root, path)
    expected = schema.get('type')
    kinds = expected if isinstance(expected, list) else [expected] if expected else []
    def matches(kind):
        return {'object': isinstance(value, dict), 'array': isinstance(value, list),
                'string': isinstance(value, str), 'integer': isinstance(value, int) and not isinstance(value, bool),
                'boolean': isinstance(value, bool), 'null': value is None}.get(kind, False)
    if kinds and not any(matches(k) for k in kinds):
        raise ValueError(f'{path}: expected {expected}')
    if 'const' in schema and value != schema['const']:
        raise ValueError(f'{path}: expected {schema["const"]!r}')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(f'{path}: unsupported value {value!r}')
    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value:
                raise ValueError(f'{path}: missing {key}')
        for key, subschema in schema.get('properties', {}).items():
            if key in value:
                validate_schema(value[key], subschema, root, f'{path}.{key}')
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            raise ValueError(f'{path}: too few entries')
        if schema.get('uniqueItems') and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            raise ValueError(f'{path}: duplicate entries')
        for n, entry in enumerate(value):
            validate_schema(entry, schema.get('items', {}), root, f'{path}[{n}]')
    if isinstance(value, str):
        if len(value.strip()) < schema.get('minLength', 0):
            raise ValueError(f'{path}: blank text')
        if schema.get('format') == 'date':
            try:
                datetime.date.fromisoformat(value)
            except ValueError as exc:
                raise ValueError(f'{path}: expected an ISO calendar date') from exc
    if isinstance(value, int) and not isinstance(value, bool) and value < schema.get('minimum', value):
        raise ValueError(f'{path}: below minimum')


def validate_record(data):
    schema = json.loads((ROOT / 'assets/round-record.schema.json').read_text(encoding='utf-8'))
    validate_schema(data, schema, schema)
    ids = {}
    for section in ['evidence', 'reviewers', 'needs', 'candidates']:
        entries = data[section]
        section_ids = [e['id'] for e in entries]
        if len(section_ids) != len(set(section_ids)):
            raise ValueError(f'{section}: duplicate identifiers')
        ids[section] = set(section_ids)
    def links(values, target, path):
        unknown = set(values) - ids[target]
        if unknown:
            raise ValueError(f'{path}: unknown {target} identifiers: {sorted(unknown)}')
    for section in ['reviewers', 'needs']:
        for entry in data[section]:
            links(entry['evidence_ids'], 'evidence', entry['id'])
            if section == 'needs':
                links(entry['reviewer_ids'], 'reviewers', entry['id'])
    for candidate in data['candidates']:
        links(candidate['need_ids'], 'needs', candidate['id'])
        if candidate['decision'] in ['prototype', 'extend'] and not candidate['need_ids']:
            raise ValueError(f'{candidate["id"]}: connect the intervention to a customer need')
    for discussion in data['disagreements']:
        links([p['reviewer_id'] for p in discussion['positions']], 'reviewers', 'disagreement')
    for evidence in data['evidence']:
        if evidence.get('url'):
            url = urlsplit(evidence['url'])
            if url.scheme not in ['http', 'https'] or not url.netloc or url.username or url.password:
                raise ValueError(f'{evidence["id"]}: source URL must be http(s) without embedded credentials')
    return data


PAGE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Product review canvas</title>
<style>
:root{--ink:#173e43;--muted:#657a7c;--line:#dce4e2;--surface:#fff;--bg:#f5f6f2;--accent:#145864;--tint:#e8f0ed;--warn:#805f2e}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 system-ui,sans-serif}a{color:var(--accent)}button,input{font:inherit}button{cursor:pointer}.wrap{width:min(1320px,92vw);margin:auto;padding:30px 0 60px}.top{display:flex;justify-content:space-between;gap:20px;border-bottom:1px solid var(--line);padding-bottom:20px;color:var(--muted);font-size:12px}.eyebrow{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--muted)}h1{font:400 clamp(30px,4vw,49px)/1.2 Georgia,serif;max-width:1000px;margin:20px 0}h2{font:400 28px/1.3 Georgia,serif;margin:0 0 15px}h3{font:400 23px/1.35 Georgia,serif;margin:14px 0}h4{font-size:11px;text-transform:uppercase;letter-spacing:.5px;margin:20px 0 6px}p{margin:10px 0}.notice{padding:17px 20px;background:#f6efdf;color:var(--warn);border:1px solid #e8ddc5;border-radius:10px;margin:25px 0}.notice p{font-size:13px}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin:25px 0}.stat,.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:23px;min-width:0}.stat strong{display:block;font:32px Georgia,serif;color:var(--accent)}.stat span{font-size:12px;color:var(--muted)}section{margin-top:34px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;align-items:start}.candidates{grid-template-columns:repeat(2,minmax(0,1fr))}.card p,.card li{font-size:13px;color:var(--muted)}.card ul{padding-left:20px}.pill{display:inline-flex;background:var(--tint);color:var(--accent);border-radius:5px;padding:3px 8px;font-size:10px;letter-spacing:.3px}.pill.warn{background:#f6efdf;color:var(--warn)}.role-top{display:flex;justify-content:space-between;gap:12px}.role-job{min-height:45px}.value{padding:12px 15px;background:#f3f6ef;border-radius:7px}.value p{margin:4px 0}details{margin-top:17px;border-top:1px solid var(--line);padding-top:13px}summary{cursor:pointer;color:var(--accent);font-size:12px}.filters{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}.filters button{border:1px solid var(--line);background:white;border-radius:7px;padding:8px 12px;color:var(--muted);font-size:12px}.filters button[aria-pressed=true]{background:var(--accent);color:white;border-color:var(--accent)}.search{width:100%;max-width:420px;display:block;margin:12px 0}.search span{display:block;font-size:12px;color:var(--muted);margin-bottom:5px}.search input{width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:7px;background:white;color:var(--ink)}.count{font-size:12px;color:var(--muted)}.empty{padding:30px;background:white;border:1px dashed var(--line);border-radius:10px}.ledger{display:grid;gap:12px}.source{padding:17px;border-left:3px solid #b9ceca;background:white;overflow-wrap:anywhere}.source p{font-size:13px}.source small{color:var(--muted)}footer{margin-top:40px;color:var(--muted);font-size:12px}*:focus-visible{outline:3px solid #6aa7b0;outline-offset:3px}.checks{font-size:13px;padding-left:20px}.skip{position:absolute;left:-9999px}.skip:focus{left:15px;top:10px;background:white;padding:10px;z-index:5}@media(max-width:1000px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:650px){.grid,.candidates{grid-template-columns:1fr}.stats{grid-template-columns:1fr 1fr}.card{padding:20px}.top{display:block}.wrap{width:90vw}h1{font-size:34px}}
</style></head><body><a class="skip" href="#main">Skip to review</a><main id="main" class="wrap"><header class="top"><strong id="project"></strong><span id="round"></span></header><span class="eyebrow">Product research → workflow experiment</span><h1 id="question"></h1><div class="notice" id="method"></div><div class="stats" id="stats"></div><section id="scenarios-section" hidden><h2>Scenarios reviewed</h2><div class="grid candidates" id="scenarios"></div></section><section id="unknowns-section" class="card" hidden><h2>Still unknown</h2><ul id="unknowns"></ul></section><section><h2>Candidate interventions</h2><div class="grid candidates" id="candidates"></div></section><section><h2>Customer needs to test</h2><div class="grid" id="needs"></div></section><section><h2>Perspectives on the work</h2><p class="count">Role lenses are not interview counts or independent demand signals.</p><div id="filters" class="filters" role="group" aria-label="Filter reviewer perspectives"></div><label class="search"><span>Search roles and jobs</span><input id="search" type="search" placeholder="Role, job or objection"></label><p id="count" class="count" aria-live="polite"></p><div class="grid" id="roles"></div></section><section><h2>Disagreements and alternatives</h2><div class="grid candidates" id="disagreements"></div></section><section class="card"><h2>Next real-world validation</h2><ul id="next"></ul></section><section><h2>Evidence and its limits</h2><div class="ledger" id="evidence"></div></section><section class="card" id="implementation"></section><footer>Structured synthesis. Sources support only the claims identified; simulated agreement does not establish customer demand.</footer></main>
<script id="round-data" type="application/json">__ROUND_JSON__</script>
<script>
const record=JSON.parse(document.getElementById('round-data').textContent),byId=Object.fromEntries(record.reviewers.map(r=>[r.id,r])),needsById=Object.fromEntries(record.needs.map(n=>[n.id,n]));
const e=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])),list=a=>a.map(x=>`<li>${e(x)}</li>`).join(''),refs=a=>a.length?a.map(e).join(', '):'No supporting source linked; hypothesis remains ungrounded.';
const set=(id,html)=>document.getElementById(id).innerHTML=html;
function detailTree(v){if(Array.isArray(v))return `<ul>${v.map(x=>`<li>${typeof x==='object'?detailTree(x):e(x)}</li>`).join('')}</ul>`;if(v&&typeof v==='object')return Object.entries(v).map(([k,x])=>`<h4>${e(k.replaceAll('_',' '))}</h4>${detailTree(x)}`).join('');return `<p>${e(v)}</p>`}
document.title=record.project.name+' · Review canvas';document.getElementById('project').textContent=record.project.name;document.getElementById('round').textContent=`Round ${record.project.round} · ${record.project.date}${record.project.mode?' · '+record.project.mode:''}`;document.getElementById('question').textContent=record.project.question;
set('method',`<strong>${record.method.kind==='simulated'?'Simulated panel · not customer validation':'Research synthesis · inspect evidence types'}</strong><p>${e(record.method.summary)}</p><details><summary>Method limits</summary><ul>${list(record.method.limitations)}</ul></details>`);
set('stats',[[record.reviewers.length,'Represented perspectives'],[record.reviewers.filter(r=>r.new).length,'New this round'],[record.needs.length,'Needs to investigate'],[record.candidates.filter(c=>['prototype','extend'].includes(c.decision)).length,'Prototype / extend proposals']].map(([v,label])=>`<div class="stat"><strong>${v}</strong><span>${label}</span></div>`).join(''));
set('candidates',record.candidates.map(c=>`<article class="card"><span class="pill ${['defer','reject'].includes(c.decision)?'warn':''}">Proposed direction: ${e(c.decision)}</span><h3>${e(c.name)}</h3><p>${e(c.rationale)}</p><p><strong>Need:</strong> ${c.need_ids.map(id=>e(needsById[id].need)).join('; ')}</p><details><summary>Inputs, behavior and tradeoffs</summary>${c.beneficiary?`<h4>Who benefits</h4><p>${e(c.beneficiary)}</p>`:''}${c.trigger?`<h4>Trigger</h4><p>${e(c.trigger)}</p>`:''}<h4>Inputs</h4><ul>${list(c.inputs)}</ul><h4>Output</h4><p>${e(c.output)}</p><h4>Human decision</h4><p>${e(c.human_decision)}</p><h4>Failure cases</h4><ul>${list(c.failure_cases)}</ul>${c.assumptions?`<h4>Assumptions</h4><ul>${list(c.assumptions)}</ul>`:''}${c.experiment_design?`<h4>Proposed experiment design</h4>${detailTree(c.experiment_design)}`:''}<h4>Dissent / alternative</h4><p>${e(c.dissent)}</p></details></article>`).join('')||'<p class="empty">No intervention decisions recorded.</p>');
set('needs',record.needs.map(n=>`<article class="card"><span class="eyebrow">${e(n.workflow)}</span><h3>${e(n.need)}</h3><p>${e(n.uncertainty)}</p><p><strong>Perspectives:</strong> ${n.reviewer_ids.map(id=>e(byId[id].role)).join(', ')||'Not specified'}</p><p><strong>Evidence IDs:</strong> ${refs(n.evidence_ids)}</p></article>`).join(''));
let filter='All';const filters=['All','New this round','operator','buyer','recipient','referrer','affected','boundary'];set('filters',filters.map(f=>`<button type="button" data-filter="${f}" aria-pressed="${f==='All'}">${e(f)}</button>`).join(''));
function showRoles(){const term=document.getElementById('search').value.toLowerCase(),shown=record.reviewers.filter(r=>(filter==='All'||(filter==='New this round'?r.new:r.relationships.includes(filter)))&&[r.role,r.job,r.objection,r.incentive].join(' ').toLowerCase().includes(term));document.getElementById('count').textContent=`${shown.length} of ${record.reviewers.length} represented perspectives`;set('roles',shown.map(r=>`<article class="card"><div class="role-top"><span class="eyebrow">${e(r.relationships.join(' · '))}</span><span class="pill">${e(r.basis)}${r.new?' · new':''}</span></div><h3>${e(r.role)}</h3><p class="role-job">${e(r.job)}</p><div class="value"><span class="eyebrow">Possible incentive</span><p>${e(r.incentive)}</p></div><details><summary>Objection & disconfirming question</summary>${r.trigger?`<h4>Trigger</h4><p>${e(r.trigger)}</p>`:''}${r.workaround?`<h4>Existing workaround</h4><p>${e(r.workaround)}</p>`:''}${r.responsibility_boundary?`<h4>Responsibility boundary</h4><p>${e(r.responsibility_boundary)}</p>`:''}<h4>Objection</h4><p>${e(r.objection)}</p><h4>Ask a real participant</h4><p>${e(r.disconfirming_question)}</p><p><strong>Evidence IDs:</strong> ${refs(r.evidence_ids)}</p></details></article>`).join('')||'<p class="empty">No perspectives match this filter.</p>')}
document.getElementById('filters').addEventListener('click',ev=>{const b=ev.target.closest('[data-filter]');if(!b)return;filter=b.dataset.filter;for(const el of document.querySelectorAll('[data-filter]'))el.setAttribute('aria-pressed',el.dataset.filter===filter);showRoles()});document.getElementById('search').addEventListener('input',showRoles);showRoles();
set('disagreements',record.disagreements.map(d=>`<article class="card"><h3>${e(d.issue)}</h3>${d.positions.map(p=>`<p><strong>${e(byId[p.reviewer_id].role)}:</strong> ${e(p.position)}</p>`).join('')}<h4>Decision for this round</h4><p>${e(d.resolution)}</p><h4>Still unknown</h4><p>${e(d.uncertainty)}</p></article>`).join('')||'<p class="empty">No disagreement recorded. This does not establish independent consensus.</p>');
if(record.scenarios?.length){document.getElementById('scenarios-section').hidden=false;set('scenarios',record.scenarios.map(s=>`<article class="card"><span class="pill">${s.fictional?'Fictional scenario':'Provided scenario · inspect evidence'}</span><h3>${e(s.id)}</h3><ul>${list(s.records)}</ul><p>${e(s.review)}</p></article>`).join(''))}if(record.unknowns?.length){document.getElementById('unknowns-section').hidden=false;set('unknowns',list(record.unknowns))}set('next',list(record.next_validation));set('evidence',record.evidence.map(s=>`<article class="source"><span class="pill">${e(s.kind)}</span> <strong>${e(s.id)}</strong><p>${e(s.claim)}</p><small>${e(s.source)}${s.accessed?' · accessed '+e(s.accessed):''}</small>${s.url?`<p><a href="${e(s.url)}" target="_blank" rel="noopener noreferrer">Open supporting source ↗</a></p>`:''}</article>`).join('')||'<p class="empty">No evidence records supplied. Treat the synthesis as ungrounded hypotheses.</p>');
const imp=record.implementation;set('implementation',imp?`<h2>Implementation and verification</h2><p>Status: ${e(imp.status||'not specified')}</p><ul>${list(imp.entry_points||[])}</ul><ul class="checks">${(imp.checks||[]).map(c=>`<li><strong>${e(c.result)} · ${e(c.name)}:</strong> ${e(c.detail)}</li>`).join('')}</ul>`:'<h2>Implementation not recorded</h2><p>This canvas does not imply a prototype was built or tested.</p>');
</script></body></html>'''


def render(data):
    validate_record(data)
    encoded = json.dumps(data, ensure_ascii=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    return PAGE.replace('__ROUND_JSON__', encoded, 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--out', type=Path, help='HTML destination; existing files require --overwrite')
    parser.add_argument('--check', action='store_true', help='Validate only')
    parser.add_argument('--overwrite', action='store_true', help='Explicitly replace an existing output file')
    args = parser.parse_args()
    try:
        data = validate_record(json.loads(args.record.read_text(encoding='utf-8')))
        if args.check:
            print(f'Valid round record: {len(data["reviewers"])} represented perspectives; factual claims not verified.')
            return
        if not args.out:
            parser.error('--out is required unless --check is used')
        if args.out.resolve() == args.record.resolve():
            raise ValueError('Output must differ from the input record')
        if args.out.exists() and not args.overwrite:
            raise ValueError('Output exists; choose another path or use --overwrite')
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(render(data), encoding='utf-8')
        print(f'Created offline canvas: {args.out}')
    except (OSError, ValueError, KeyError) as exc:
        print(f'Cannot render panel: {exc}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
