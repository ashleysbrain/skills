#!/usr/bin/env python3
"""Generate gg-process-graph-data.js from the real FLEET_REGISTRY.

Usage:
    cd /<workspace>
    python3 skills-library/software-development/3d-process-flow-graph/scripts/generate-graph-data.py > gg-process-graph-data.js

This ensures every engine in the fleet is included in the 3D graph.
Never hardcode engine lists — always generate from the registry.
"""
import sys, os, json, re

# Add agent-organism to path
sys.path.insert(0, os.path.expanduser('~/your-workspace/agent-organism'))
from ecs import FLEET_REGISTRY

# Body system color mapping
BODY_SYSTEM_MAP = {
    'nervous': 'nervous', 'cardiovascular': 'cardiovascular',
    'skeletal': 'connective', 'connective': 'connective',
    'reproductive': 'reproductive', 'digestive': 'digestive',
    'respiratory': 'respiratory', 'muscular': 'muscular',
    'endocrine': 'endocrine', 'lymphatic': 'immune', 'immune': 'immune',
    'integumentary': 'integumentary', 'urinary': 'urinary',
    'diagnostic': 'sensory', 'sensory': 'sensory',
    'regulatory': 'regulatory', 'creative_visual': 'creative_visual',
}

# Name overrides for engines where the scientist name doesn't match the directory
NAME_OVERRIDES = {
    'ds-j-eccles': 'DS J Eccles',
    'ds-ramon-cajal': 'the specialist engine',
    'ds-ecs-compliance-agent': 'the specialist engine',
    'ds-eccles-agent': 'DS J Eccles',
    'ds-sherman-agent': 'the specialist engine',
    'ds-rakic-agent': 'the specialist engine',
    'ds-cannon-agent': 'the specialist engine',
    'ds-osler-agent': 'the specialist engine',
    'ds-golgi-agent': 'the specialist engine',
    'ds-rontgen-engine': 'DS Röntgen',
    'ds-creative-cortex-engine': 'the specialist engine',
    'ds-design-engine': 'the specialist engine',
    'ds-clinical-engine': 'the specialist engine',
    'ds-lovelace-engine': 'the specialist engine',
    'ds-neural-tube-engine': 'the specialist engine',
    'ds-genome-engine': 'the specialist engine',
    'ds-placenta-engine': 'the specialist engine',
    'ds-reproductive-engine': 'the specialist engine',
    'ds-trophoblast-engine': 'the specialist engine',
    'ds-thalamus-engine': 'the specialist engine',
    'ds-oncology-engine': 'the specialist engine',
    'ds-speech-synthesis-engine': 'the specialist engine AG',
    'ds-wave-coaching-engine': 'the specialist engine',
    'ds-quartz-engine': 'the specialist engine',
    'ds-sutherland-engine': 'the specialist engine',
    'ds-simard-engine': 'the specialist engine',
    'ds-bell-engine': 'the specialist engine',
}

# Legacy alias nodes (engines referenced in ops platform but not in FLEET_REGISTRY)
LEGACY_ALIASES = [
    {'id': 'eng_dudley', 'name': 'the specialist engine', 'desc': 'Vocoder speech synthesis (alias of the specialist engine AG)', 'body_system': 'nervous', 'ecs_code': 'DS-SPEECH-SYNTHESIS-ENGINE', 'port': 8103},
    {'id': 'eng_hall', 'name': 'the specialist engine', 'desc': 'Circadian rhythm (legacy alias of the specialist engine)', 'body_system': 'regulatory', 'ecs_code': 'DS-QUARTZ-ENGINE', 'port': 8089},
]

def generate():
    nodes = []
    
    # Sources
    for src in [
        ('src_user', 'User Input', 'Telegram, dashboard, API input'),
        ('src_cron', 'Cron Trigger', 'Scheduled task from the specialist engine lattice'),
        ('src_alert', 'Alert Trigger', 'Self-healing or monitoring alert'),
    ]:
        nodes.append(f"{{id:'{src[0]}',name:'{src[1]}',type:'source',desc:'{src[2]}'}}")
    
    # Router
    nodes.append("{id:'rtr_sherman',name:'the specialist engine',type:'router',engine:'the specialist engine',desc:'Thalamocortical routing dispatch',body_system:'nervous',ecs_code:'DS-SHERMAN-AGENT',port:null,routes:[{condition:'creative',target:'eng_goethe'},{condition:'design',target:'eng_goethe'},{condition:'code',target:'eng_rakic'},{condition:'audit',target:'eng_ecs_compliance'},{condition:'health',target:'eng_clinical'},{condition:'message',target:'eng_harvey'}]}")
    
    # Engines from FLEET_REGISTRY
    for dir_name, info in sorted(FLEET_REGISTRY.items()):
        if dir_name == 'ds-seed-engine':
            continue  # Legacy alias of ds-reproductive-engine
        
        scientist = info.get('scientist', dir_name)
        port = info.get('port', None)
        body_system_raw = info.get('body_system', info.get('system', info.get('tissue', 'nervous')))
        body_system = BODY_SYSTEM_MAP.get(body_system_raw, 'nervous')
        desc = info.get('description', info.get('desc', ''))
        if desc:
            desc = desc[:80].replace("'", "\\'").replace("\n", " ")
        else:
            desc = dir_name.replace("-", " ").title()
        
        node_id = 'eng_' + dir_name.replace('ds-', '').replace('-engine', '').replace('-agent', '').replace('-', '_')
        short_name = NAME_OVERRIDES.get(dir_name, 'DS ' + scientist.split()[-1])
        port_str = str(port) if port else 'null'
        ecs_code = dir_name.upper().replace('-', '-')
        
        nodes.append(f"{{id:'{node_id}',name:'{short_name}',type:'engine',desc:'{desc}',body_system:'{body_system}',ecs_code:'{ecs_code}',port:{port_str}}}")
    
    # Legacy aliases
    for alias in LEGACY_ALIASES:
        nodes.append(f"{{id:'{alias['id']}',name:'{alias['name']}',type:'engine',desc:'{alias['desc']}',body_system:'{alias['body_system']}',ecs_code:'{alias['ecs_code']}',port:{alias['port']}}}")
    
    print(f"// GRAPH DATA MODEL — generated from FLEET_REGISTRY ({len(FLEET_REGISTRY)} engines)")
    print(f"// {len(nodes)} total nodes (engines + gates + sources + sinks + router)")
    print(f"// DO NOT EDIT MANUALLY — regenerate with scripts/generate-graph-data.py")
    print()
    print("var NODE_TYPES={engine:{color:'#6366f1',shape:'sphere',label:'Engine'},gate:{color:'#fbbf24',shape:'octahedron',label:'Gate'},router:{color:'#818cf8',shape:'torus',label:'Router'},source:{color:'#22c55e',shape:'sphere',label:'Source'},sink:{color:'#5a6a8a',shape:'sphere',label:'Sink'}};")
    print("var EDGE_TYPES={sequential:{color:'rgba(232,213,160,0.4)',label:'Sequential',particle:true},parallel_fork:{color:'rgba(129,140,248,0.4)',label:'Fork',particle:true},parallel_join:{color:'rgba(74,214,180,0.4)',label:'Join',particle:true},conditional:{color:'rgba(251,191,36,0.35)',label:'Conditional',particle:true},feedback:{color:'rgba(239,68,68,0.3)',label:'Feedback',particle:true},cross_flow:{color:'rgba(99,102,241,0.25)',label:'Cross-flow',particle:false},tissue:{color:'rgba(90,106,138,0.12)',label:'Tissue',particle:false}};")
    print("var BODY_SYSTEMS={nervous:'#6366f1',cardiovascular:'#ef4444',creative_visual:'#e8d5a0',digestive:'#22c55e',immune:'#fbbf24',regulatory:'#4ad6b4',reproductive:'#c4956a',connective:'#5a6a8a',sensory:'#818cf8',respiratory:'#06b6d4',muscular:'#f97316',endocrine:'#a855f7',integumentary:'#ec4899',urinary:'#0ea5e9'};")
    print(f"var ONTOLOGY={{nodes:[")
    print(",\n".join(nodes))
    print("],")
    print("""edges:[
// SEMANTIC (tissue connections)
{source:'eng_goethe',target:'eng_wernicke',type:'tissue',layer:'semantic'},
{source:'eng_goethe',target:'eng_design',type:'tissue',layer:'semantic'},
{source:'eng_wernicke',target:'eng_bell',type:'tissue',layer:'semantic'},
{source:'eng_bell',target:'eng_luria',type:'tissue',layer:'semantic'},
{source:'eng_luria',target:'eng_harvey',type:'tissue',layer:'semantic'},
{source:'eng_harvey',target:'eng_simard',type:'tissue',layer:'semantic'},
{source:'eng_harvey',target:'eng_neural_tube',type:'tissue',layer:'semantic'},
{source:'eng_tawara',target:'eng_harvey',type:'tissue',layer:'semantic'},
{source:'eng_creative_cortex',target:'eng_goethe',type:'tissue',layer:'semantic'},
{source:'eng_quartz',target:'eng_tawara',type:'tissue',layer:'semantic'},
{source:'eng_quartz',target:'eng_allostasis',type:'tissue',layer:'semantic'},
{source:'eng_allostasis',target:'eng_clinical',type:'tissue',layer:'semantic'},
{source:'eng_clinical',target:'eng_rontgen',type:'tissue',layer:'semantic'},
{source:'eng_rontgen',target:'eng_sherrington',type:'tissue',layer:'semantic'},
{source:'eng_sherrington',target:'eng_semmelweis',type:'tissue',layer:'semantic'},
{source:'eng_rakic',target:'eng_ecs_compliance',type:'tissue',layer:'semantic'},
{source:'eng_rakic',target:'eng_bichat',type:'tissue',layer:'semantic'},
{source:'eng_rakic',target:'eng_turing',type:'tissue',layer:'semantic'},
{source:'eng_ecs_compliance',target:'eng_eccles',type:'tissue',layer:'semantic'},
{source:'eng_ecs_compliance',target:'eng_trophoblast',type:'tissue',layer:'semantic'},
{source:'eng_genome',target:'eng_reproductive',type:'tissue',layer:'semantic'},
{source:'eng_reproductive',target:'eng_placenta',type:'tissue',layer:'semantic'},
{source:'eng_lyapunov',target:'eng_metchnikoff',type:'tissue',layer:'semantic'},
{source:'eng_metchnikoff',target:'eng_burnet',type:'tissue',layer:'semantic'},
{source:'eng_burnet',target:'eng_simard',type:'tissue',layer:'semantic'},
{source:'eng_simard',target:'eng_trophoblast',type:'tissue',layer:'semantic'},
{source:'eng_sperry',target:'eng_goethe',type:'tissue',layer:'semantic'},
{source:'eng_dudley',target:'eng_speech_synthesis',type:'tissue',layer:'semantic'},
{source:'eng_hall',target:'eng_quartz',type:'tissue',layer:'semantic'},
{source:'eng_osler',target:'eng_clinical',type:'tissue',layer:'semantic'},
// KINETIC — Creative Production
{source:'src_user',target:'rtr_sherman',type:'sequential',layer:'kinetic',pipeline:'creative_production'},
{source:'rtr_sherman',target:'gate_entry',type:'sequential',layer:'kinetic',pipeline:'creative_production'},
{source:'gate_entry',target:'eng_goethe',type:'sequential',layer:'kinetic',pipeline:'creative_production'},
{source:'eng_goethe',target:'gate_brand',type:'sequential',layer:'kinetic',pipeline:'creative_production'},
{source:'gate_brand',target:'eng_wernicke',type:'sequential',layer:'kinetic',pipeline:'creative_production'},
{source:'eng_wernicke',target:'gate_voice',type:'sequential',layer:'kinetic',pipeline:'creative_production'},
{source:'gate_voice',target:'eng_kosslyn',type:'conditional',layer:'kinetic',pipeline:'creative_production',condition:'image needed'},
{source:'gate_voice',target:'eng_bell',type:'conditional',layer:'kinetic',pipeline:'creative_production',condition:'text only'},
{source:'eng_kosslyn',target:'eng_bell',type:'parallel_join',layer:'kinetic',pipeline:'creative_production'},
{source:'eng_bell',target:'gate_render',type:'sequential',layer:'kinetic',pipeline:'creative_production'},
{source:'gate_render',target:'eng_luria',type:'sequential',layer:'kinetic',pipeline:'creative_production'},
{source:'eng_luria',target:'gate_luria',type:'sequential',layer:'kinetic',pipeline:'creative_production'},
{source:'gate_luria',target:'eng_wernicke',type:'feedback',layer:'kinetic',pipeline:'creative_production',condition:'rejected'},
{source:'gate_luria',target:'eng_harvey',type:'sequential',layer:'kinetic',pipeline:'creative_production',condition:'approved'},
{source:'eng_harvey',target:'gate_delivery',type:'sequential',layer:'kinetic',pipeline:'creative_production'},
{source:'gate_delivery',target:'sink_telegram',type:'sequential',layer:'kinetic',pipeline:'creative_production'},
{source:'gate_delivery',target:'sink_pdf',type:'sequential',layer:'kinetic',pipeline:'creative_production'},
// KINETIC — Design Pipeline
{source:'rtr_sherman',target:'eng_goethe',type:'conditional',layer:'kinetic',pipeline:'design_pipeline',condition:'design task'},
{source:'eng_goethe',target:'gate_brand',type:'sequential',layer:'kinetic',pipeline:'design_pipeline'},
{source:'gate_brand',target:'eng_design',type:'sequential',layer:'kinetic',pipeline:'design_pipeline'},
{source:'eng_design',target:'eng_sperry',type:'sequential',layer:'kinetic',pipeline:'design_pipeline'},
{source:'eng_sperry',target:'eng_bell',type:'sequential',layer:'kinetic',pipeline:'design_pipeline'},
{source:'eng_bell',target:'gate_render',type:'sequential',layer:'kinetic',pipeline:'design_pipeline'},
{source:'gate_render',target:'eng_luria',type:'sequential',layer:'kinetic',pipeline:'design_pipeline'},
{source:'eng_luria',target:'gate_luria',type:'sequential',layer:'kinetic',pipeline:'design_pipeline'},
// KINETIC — Social Distribution
{source:'eng_wernicke',target:'gate_voice',type:'sequential',layer:'kinetic',pipeline:'social_distribution'},
{source:'gate_voice',target:'eng_luria',type:'sequential',layer:'kinetic',pipeline:'social_distribution'},
{source:'eng_luria',target:'gate_luria',type:'sequential',layer:'kinetic',pipeline:'social_distribution'},
{source:'gate_luria',target:'eng_harvey',type:'sequential',layer:'kinetic',pipeline:'social_distribution'},
{source:'eng_harvey',target:'eng_simard',type:'sequential',layer:'kinetic',pipeline:'social_distribution'},
{source:'eng_simard',target:'gate_auth',type:'sequential',layer:'kinetic',pipeline:'social_distribution'},
{source:'gate_auth',target:'sink_telegram',type:'sequential',layer:'kinetic',pipeline:'social_distribution'},
// KINETIC — Engine Evolution
{source:'rtr_sherman',target:'eng_rakic',type:'conditional',layer:'kinetic',pipeline:'engine_evolution',condition:'code task'},
{source:'eng_rakic',target:'gate_arch',type:'sequential',layer:'kinetic',pipeline:'engine_evolution'},
{source:'gate_arch',target:'eng_ecs_compliance',type:'sequential',layer:'kinetic',pipeline:'engine_evolution'},
{source:'eng_ecs_compliance',target:'gate_ecs',type:'sequential',layer:'kinetic',pipeline:'engine_evolution'},
{source:'gate_ecs',target:'eng_bichat',type:'parallel_fork',layer:'kinetic',pipeline:'engine_evolution'},
{source:'gate_ecs',target:'eng_turing',type:'parallel_fork',layer:'kinetic',pipeline:'engine_evolution'},
{source:'eng_bichat',target:'gate_wiring',type:'parallel_join',layer:'kinetic',pipeline:'engine_evolution'},
{source:'eng_turing',target:'gate_wiring',type:'parallel_join',layer:'kinetic',pipeline:'engine_evolution'},
{source:'gate_wiring',target:'eng_eccles',type:'sequential',layer:'kinetic',pipeline:'engine_evolution'},
{source:'eng_eccles',target:'eng_harvey',type:'sequential',layer:'kinetic',pipeline:'engine_evolution'},
{source:'eng_harvey',target:'sink_fleet',type:'sequential',layer:'kinetic',pipeline:'engine_evolution'},
// KINETIC — Fleet Audit
{source:'src_cron',target:'eng_ecs_compliance',type:'sequential',layer:'kinetic',pipeline:'fleet_audit'},
{source:'eng_ecs_compliance',target:'gate_ecs',type:'sequential',layer:'kinetic',pipeline:'fleet_audit'},
{source:'gate_ecs',target:'eng_rontgen',type:'sequential',layer:'kinetic',pipeline:'fleet_audit'},
{source:'eng_rontgen',target:'gate_scan',type:'sequential',layer:'kinetic',pipeline:'fleet_audit'},
{source:'gate_scan',target:'eng_sherrington',type:'sequential',layer:'kinetic',pipeline:'fleet_audit'},
{source:'eng_sherrington',target:'eng_clinical',type:'sequential',layer:'kinetic',pipeline:'fleet_audit'},
{source:'eng_clinical',target:'gate_clinical',type:'sequential',layer:'kinetic',pipeline:'fleet_audit'},
{source:'gate_clinical',target:'eng_harvey',type:'sequential',layer:'kinetic',pipeline:'fleet_audit'},
{source:'eng_harvey',target:'sink_audit',type:'sequential',layer:'kinetic',pipeline:'fleet_audit'},
// KINETIC — Health Scoring
{source:'src_cron',target:'eng_quartz',type:'sequential',layer:'kinetic',pipeline:'health_scoring'},
{source:'eng_quartz',target:'eng_allostasis',type:'sequential',layer:'kinetic',pipeline:'health_scoring'},
{source:'eng_allostasis',target:'eng_clinical',type:'sequential',layer:'kinetic',pipeline:'health_scoring'},
{source:'eng_clinical',target:'gate_clinical',type:'sequential',layer:'kinetic',pipeline:'health_scoring'},
{source:'gate_clinical',target:'eng_harvey',type:'sequential',layer:'kinetic',pipeline:'health_scoring'},
{source:'eng_harvey',target:'sink_telegram',type:'sequential',layer:'kinetic',pipeline:'health_scoring'},
// KINETIC — Organism Birth
{source:'eng_genome',target:'eng_reproductive',type:'sequential',layer:'kinetic',pipeline:'organism_birth'},
{source:'eng_reproductive',target:'eng_placenta',type:'sequential',layer:'kinetic',pipeline:'organism_birth'},
{source:'eng_placenta',target:'eng_metchnikoff',type:'parallel_fork',layer:'kinetic',pipeline:'organism_birth'},
{source:'eng_placenta',target:'eng_trophoblast',type:'parallel_fork',layer:'kinetic',pipeline:'organism_birth'},
{source:'eng_metchnikoff',target:'eng_burnet',type:'sequential',layer:'kinetic',pipeline:'organism_birth'},
{source:'eng_trophoblast',target:'eng_burnet',type:'parallel_join',layer:'kinetic',pipeline:'organism_birth'},
{source:'eng_burnet',target:'eng_simard',type:'sequential',layer:'kinetic',pipeline:'organism_birth'},
{source:'eng_simard',target:'eng_lyapunov',type:'sequential',layer:'kinetic',pipeline:'organism_birth'},
// KINETIC — Self-Healing Loop
{source:'src_alert',target:'eng_lyapunov',type:'sequential',layer:'kinetic',pipeline:'self_healing'},
{source:'eng_lyapunov',target:'eng_metchnikoff',type:'sequential',layer:'kinetic',pipeline:'self_healing'},
{source:'eng_metchnikoff',target:'eng_burnet',type:'sequential',layer:'kinetic',pipeline:'self_healing'},
{source:'eng_burnet',target:'eng_simard',type:'feedback',layer:'kinetic',pipeline:'self_healing',condition:'antibody propagation'},
{source:'eng_lyapunov',target:'gate_healing',type:'sequential',layer:'kinetic',pipeline:'self_healing'},
// KINETIC — VERITAS Validation
{source:'eng_popper',target:'gate_veritas',type:'sequential',layer:'kinetic',pipeline:'veritas_validation'},
{source:'gate_veritas',target:'eng_lovelace',type:'conditional',layer:'kinetic',pipeline:'veritas_validation',condition:'passed'},
{source:'gate_veritas',target:'eng_popper',type:'feedback',layer:'kinetic',pipeline:'veritas_validation',condition:'failed'},
// KINETIC — Voice Input Pipeline
{source:'src_user',target:'eng_edison',type:'sequential',layer:'kinetic',pipeline:'voice_input'},
{source:'eng_edison',target:'eng_gutenberg',type:'sequential',layer:'kinetic',pipeline:'voice_input'},
{source:'eng_gutenberg',target:'rtr_sherman',type:'sequential',layer:'kinetic',pipeline:'voice_input'},
{source:'eng_speech_synthesis',target:'sink_speech',type:'sequential',layer:'kinetic',pipeline:'voice_input'},
// KINETIC — SaaS Sync
{source:'rtr_sherman',target:'eng_ecs_compliance',type:'sequential',layer:'kinetic',pipeline:'saas_sync'},
{source:'eng_ecs_compliance',target:'eng_harvey',type:'sequential',layer:'kinetic',pipeline:'saas_sync'},
{source:'eng_harvey',target:'gate_auth',type:'sequential',layer:'kinetic',pipeline:'saas_sync'},
{source:'gate_auth',target:'eng_ecs_compliance',type:'sequential',layer:'kinetic',pipeline:'saas_sync'},
{source:'eng_ecs_compliance',target:'gate_integrity',type:'sequential',layer:'kinetic',pipeline:'saas_sync'},
// KINETIC — App Action
{source:'rtr_sherman',target:'eng_dudley',type:'conditional',layer:'kinetic',pipeline:'app_action',condition:'app target'},
{source:'eng_dudley',target:'gate_format',type:'sequential',layer:'kinetic',pipeline:'app_action'},
{source:'gate_format',target:'eng_harvey',type:'sequential',layer:'kinetic',pipeline:'app_action'},
{source:'eng_harvey',target:'sink_telegram',type:'sequential',layer:'kinetic',pipeline:'app_action'},
// CROSS-FLOW
{source:'eng_harvey',target:'eng_simard',type:'cross_flow',layer:'semantic'},
{source:'eng_luria',target:'eng_ecs_compliance',type:'cross_flow',layer:'semantic'},
{source:'eng_clinical',target:'eng_harvey',type:'cross_flow',layer:'semantic'},
{source:'eng_popper',target:'eng_luria',type:'cross_flow',layer:'semantic'},
{source:'eng_osler',target:'eng_clinical',type:'cross_flow',layer:'semantic'}
],
pipelines:[
{id:'creative_production',name:'Creative Production',color:'#e8d5a0',stages:7,desc:'Idea becomes branded artifact'},
{id:'design_pipeline',name:'Design Pipeline',color:'#818cf8',stages:6,desc:'Design-only task'},
{id:'social_distribution',name:'Social Distribution',color:'#4ad6b4',stages:6,desc:'Content across platforms'},
{id:'engine_evolution',name:'Engine Evolution',color:'#6366f1',stages:8,desc:'New engine designed and built'},
{id:'fleet_audit',name:'Fleet Audit',color:'#fbbf24',stages:8,desc:'Full organism health check'},
{id:'health_scoring',name:'Health Scoring',color:'#22c55e',stages:6,desc:'Daily wellness scoring'},
{id:'organism_birth',name:'Organism Birth',color:'#c4956a',stages:8,desc:'New organism birthed'},
{id:'self_healing',name:'Self-Healing Loop',color:'#ef4444',stages:4,desc:'Threat detected and countered'},
{id:'veritas_validation',name:'VERITAS Validation',color:'#a855f7',stages:3,desc:'Physics claim validation'},
{id:'voice_input',name:'Voice Input Pipeline',color:'#06b6d4',stages:4,desc:'Audio to text to routing'},
{id:'saas_sync',name:'SaaS Sync',color:'#0ea5e9',stages:3,desc:'Push/pull data to external SaaS platforms'},
{id:'app_action',name:'App Action',color:'#f97316',stages:3,desc:'Trigger native app or device action'}
]};""")

if __name__ == '__main__':
    generate()
