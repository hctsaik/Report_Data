const fs=require('fs');const vm=require('vm');const assert=require('assert/strict');
const context=vm.createContext({structuredClone,console});
vm.runInContext(fs.readFileSync('course-content.js','utf8')+'\n'+fs.readFileSync('scenarios.js','utf8')+'\nglobalThis.exposed={SCENARIOS,ScenarioEngine,STEPS,COURSES};',context);
const {SCENARIOS,ScenarioEngine,STEPS,COURSES}=context.exposed;
const plain=x=>JSON.parse(JSON.stringify(x));
const all=Object.values(SCENARIOS).flat();let edges=0,nodes=0;
assert.equal(all.length,16);assert.equal(COURSES.operations.lessons.length,8);assert.equal(COURSES.flow.lessons.length,10);
for(const scenario of all){
 const reached=new Set(),queue=['start'];
 while(queue.length){const id=queue.shift();if(reached.has(id))continue;reached.add(id);nodes++;
  assert.ok(scenario.nodes[id],`${scenario.id}/${id} exists`);const e=new ScenarioEngine(scenario);e.nodeId=id;const state=e.state;
  assert.ok(state.current&&state.flow&&state.lot);
  if(SCENARIOS.operations.includes(scenario)){
   const positions=Object.values(state.slots).filter(Boolean).concat(state.chamber?[state.chamber]:[]);
   assert.deepEqual(positions.sort(),['W06','W07','W08'],`${scenario.id}/${id} wafer conservation and uniqueness`);
  }
  if(state.lots)assert.deepEqual(plain(state.lots.flatMap(l=>l.wafers)).sort(),['W06','W07','W08']);
  for(let i=0;i<e.node.actions.length;i++){
   const branch=new ScenarioEngine(scenario);branch.nodeId=id;const before=JSON.stringify(branch.state),a=branch.node.actions[i];edges++;
   const ok=branch.act(i);assert.equal(ok,Boolean(a.next));assert.equal(branch.events.length,2);
   if(!a.next){assert.equal(JSON.stringify(branch.state),before,`${scenario.id}/${id} rejection mutated state`);assert.equal(branch.nodeId,id);}
   else{assert.equal(branch.nodeId,a.next);queue.push(a.next);assert.ok(scenario.nodes[a.next]);}
   branch.reset();assert.equal(branch.nodeId,'start');assert.equal(branch.events.length,1);
  }
 }
 assert.equal(reached.size,Object.keys(scenario.nodes).length,`all nodes reachable in ${scenario.id}`);
}
function engine(id){return new ScenarioEngine(all.find(s=>s.id===id));}
function actTo(e,next){const i=e.node.actions.findIndex(a=>a.next===next);assert.notEqual(i,-1);e.act(i);}
// Full journeys protect semantic contracts independently of node-shape checks.
const normal=engine('normal');for(let i=0;i<6;i++){actTo(normal,'work'+i);assert.equal(normal.state.current,STEPS[i].id);actTo(normal,i===5?'finish':'ready'+(i+1));if(i===3){assert.equal(normal.state.current,'S50');assert.notEqual(normal.state.status,'Finished');}}
assert.equal(normal.state.status,'Finished');assert.equal(normal.events.length,13);assert.equal(normal.state.done.length,6);
const run=engine('run');for(let i=0;i<3;i++){actTo(run,'run'+i);assert.equal(run.state.chamber,'W0'+(6+i));actTo(run,i===2?'data':'ready'+(i+1));assert.equal(run.state.current,'S40');}actTo(run,'verified');actTo(run,'finish');assert.equal(run.state.current,'S50');
const hold=engine('hold');actTo(hold,'one');assert.equal(hold.state.hold.length,1);actTo(hold,'finish');assert.equal(hold.state.hold.length,0);assert.equal(hold.state.current,'S40');assert.equal(hold.state.status,'Queued');
const rw=engine('rework');actTo(rw,'clean');actTo(rw,'retest');actTo(rw,'finish');assert.match(rw.state.visits,/#1 = Fail/);assert.match(rw.state.visits,/#2 = Pass/);assert.equal(rw.state.current,'S60');
const split=engine('split');actTo(split,'separated');assert.equal(split.state.lots[1].current,'R10');actTo(split,'aligned');assert.equal(split.state.lots[1].current,'S50');actTo(split,'finish');assert.equal(split.state.lot,'L023-M');assert.equal(split.state.waferIds.length,3);
const version=engine('version');actTo(version,'published');assert.equal(version.state.flow,'F-DEMO v1');actTo(version,'newlot');assert.equal(version.state.flow,'F-DEMO v1');actTo(version,'finish');assert.equal(version.state.current,'S45');assert.equal(version.state.flow,'F-DEMO v2');
const q=engine('qtime');actTo(q,'expired');q.act(0);assert.equal(q.state.qtime,45);assert.equal(q.state.status,'Hold');
const report={scenarios:all.length,nodes,edges,semanticJourneys:7,status:'PASS'};fs.mkdirSync('tests/evidence/mes-007',{recursive:true});fs.writeFileSync('tests/evidence/mes-007/state-tests.json',JSON.stringify(report,null,2));console.log(report);
