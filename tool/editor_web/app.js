/* Local single-project editor. Text is inserted through textContent or escaped attributes. */
let state, catalog, areas, sessions, token, area='mathematics', tab='questions', current=null, dirty=false, busy=false;
let liveTimer, liveRunning=false, liveQueued=false, liveVersion=0, liveResult=null, livePage=1, editVersion=0;
const $=id=>document.getElementById(id), esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const id=prefix=>prefix+'-'+crypto.randomUUID();
function status(text,error=false){$('status').textContent=text;$('status').className=error?'error':dirty?'dirty':'';}
function invalidateOutputs(){if(!$('results').hidden)$('warnings').textContent='Exportación anterior: genera de nuevo para incluir tus cambios.';$('results').hidden=true;}
function changed(){editVersion++;dirty=true;invalidateOutputs();status('Cambios sin guardar. Guarda el proyecto para conservarlos y generar el PDF.');schedulePreview();}
function resizeOptions(q,count){
 // Keep removed text and image references in the project, including JSON backups.
 q.option_drafts??={};
 while(q.options.length>count){const index=q.options.length-1;q.option_drafts[index]=q.options.pop();}
 while(q.options.length<count){const index=q.options.length;q.options.push(q.option_drafts[index]||{text:''});delete q.option_drafts[index];}
}
function schedulePreview(force=false){
 liveVersion++;clearTimeout(liveTimer);
 if(!force&&!$('live-auto').checked){$('live-status').textContent='Vista pausada. Pulsa Actualizar para ver tus cambios.';return;}
 $('live-status').textContent=liveResult?'Cambios pendientes de previsualizar…':'Preparando vista previa…';
 liveTimer=setTimeout(updatePreview,force?0:1100);
}
function focusPreview(){
 if(!liveResult)return;
 let qid=tab==='questions'?current:state.questions.find(q=>q.context===current)?.id;
 if(qid&&liveResult.page_map[qid])showLivePage(liveResult.page_map[qid]);
}
function showLivePage(number){
 if(!liveResult)return;
 livePage=Math.min(liveResult.pages,Math.max(1,Number(number)||1));
 $('live-page').value=String(livePage);$('live-prev').disabled=livePage===1;$('live-next').disabled=livePage===liveResult.pages;
 $('live-image').hidden=false;$('live-image').src='/previews/'+liveResult.id+'/'+livePage+'.png';
 $('live-image').alt='Página '+livePage+' de '+liveResult.pages+' del cuadernillo';
}
async function updatePreview(){
 if(liveRunning){liveQueued=true;return;}
 liveRunning=true;liveQueued=false;const version=liveVersion;
 $('live-status').textContent='Componiendo páginas…';$('live-panel')?.setAttribute('aria-busy','true');
 try{
  const result=await api('preview',{project:structuredClone(state)});
  if(version!==liveVersion){liveQueued=$('live-auto').checked;return;}
  liveResult=result;
  $('live-page').innerHTML=Array.from({length:result.pages},(_,i)=>`<option value="${i+1}">${i+1} de ${result.pages}</option>`).join('');
  showLivePage(livePage);focusPreview();
  $('live-warnings').textContent=[...new Set(result.warnings)].join('\n')||'Sin pendientes estructurales.';
  $('live-status').textContent='Vista actualizada · '+result.pages+' páginas · '+(dirty?'cambios aún sin guardar':'proyecto guardado');
 }catch(err){
  if(version===liveVersion)$('live-status').textContent='No se pudo actualizar: '+err.message+' La vista anterior se conserva.';
 }finally{
  liveRunning=false;$('live-panel')?.setAttribute('aria-busy','false');
  if(liveQueued){liveQueued=false;clearTimeout(liveTimer);liveTimer=setTimeout(updatePreview,250);}
 }
}
async function api(path,payload){const response=await fetch('/api/'+path,{method:'POST',headers:{'Content-Type':'application/json','X-Local-Token':token},body:JSON.stringify(payload)});const data=await response.json();if(!response.ok)throw Error(data.error||'Error del servicio');return data;}
const blank=a=>({framework:catalog.id,area:a,status:'unclassified',competency:null,process:null,claim:null,evidence:null,component:null,part:null,rationale:'',reviewer:null,reviewed_at:null});
function setClassification(q,enabled){if(!enabled)q.assessment=blank(q.area);else{q.assessment.status='proposed';if(q.area==='english')q.assessment.part=q.part;}}
function updateClassification(q,key,value){const a=q.assessment;if(a.status==='reviewed')a.status='proposed';a[key]=value||null;if(q.area==='english')a.part=q.part;if(key==='competency'){a.claim=null;a.evidence=null;a.process=null;}if(key==='claim'){a.evidence=null;if(q.area==='reading')a.process=Object.keys(catalog.areas.reading.processes).find(k=>catalog.areas.reading.processes[k].claim===a.claim)||null;}}
function renderAreaHeader(){
 const key=$('heading-area').value||'mathematics',header=state.area_headers?.[key]||{};
 $('area-title').value=header.title||'';$('area-title').placeholder=areas[key].toUpperCase();
 $('area-instructions').value=header.instructions||'';
}
function optionList(values,value,empty='Selecciona…'){return '<option value="">'+esc(empty)+'</option>'+Object.entries(values).map(([k,v])=>`<option value="${esc(k)}" ${String(k)===String(value)?'selected':''}>${esc(typeof v==='object'?v.label:v)}</option>`).join('');}
function input(label,key,value,type='text'){return `<label>${label}<input data-field="${key}" type="${type}" value="${esc(value)}"></label>`;}
function text(label,key,value){return `<label>${label}<textarea data-field="${key}">${esc(value)}</textarea></label>`;}
function select(label,key,options,value){return `<label>${label}<select data-field="${key}">${optionList(options,value)}</select></label>`;}
function imageField(obj,key){return `<div class="image-field"><label>Imagen opcional · PNG, JPG o WEBP, hasta 5 MiB<input type="file" accept="image/png,image/jpeg,image/webp" data-upload="${key}"></label>${obj.image?`<img class="thumb" src="/${esc(obj.image)}" alt="Imagen cargada"><button data-remove="${key}">Quitar imagen del contenido</button>`:'<small>Se conserva la proporción original. Revisa la legibilidad en el PDF.</small>'}</div>`;}
function getCurrent(){return state[tab].find(q=>q.id===current);}
function refresh(){
 $('code').value=state.code;$('session').value=state.session;$('time').value=state.time;
 $('sequence').textContent=sessions[state.session].map(a=>areas[a]).join(' → ');
 const headingArea=$('heading-area').value||area;
 $('heading-area').innerHTML=Object.entries(areas).map(([k,v])=>`<option value="${k}" ${k===headingArea?'selected':''}>${esc(v)}</option>`).join('');
 renderAreaHeader();
 $('area').innerHTML=Object.entries(areas).map(([k,v])=>`<option value="${k}" ${area===k?'selected':''}>${esc(v)}</option>`).join('');
 $('targets').innerHTML=Object.entries(areas).map(([k,v])=>`<label>${esc(v)}<input type="number" min="0" max="300" data-target="${k}" value="${state.targets[k]??''}" placeholder="Sin definir"></label>`).join('');
 $('targets').querySelectorAll('input').forEach(el=>el.oninput=()=>{state.targets[el.dataset.target]=el.value===''?null:Number(el.value);changed();});
 $('add').textContent=tab==='questions'?'+ Nueva pregunta':'+ Nuevo contexto';
 $('questions-tab').className=tab==='questions'?'active':'';$('contexts-tab').className=tab==='contexts'?'active':'';
 renderList();renderForm();schedulePreview();
}
function renderList(){const items=state[tab].filter(q=>q.area===area).sort((a,b)=>(a.part||0)-(b.part||0)||(a.order||0)-(b.order||0));$('list').innerHTML=items.length?items.map((q,i)=>`<button class="item ${q.id===current?'selected':''}" data-id="${q.id}"><span class="badge">${q.part?'Parte '+q.part+' · ':''}${tab==='questions'?(q.included?'Incluida':'Fuera de sesión'):'Contexto compartido'}</span><strong>${esc(tab==='questions'?q.topic||'Pregunta '+(i+1):q.title||'Sin título')}</strong><small>${esc(q.stem||q.text||'Sin contenido todavía')}</small></button>`).join(''):'<p class="note">Todavía no hay contenido en esta área.</p>';$('list').querySelectorAll('button').forEach(el=>el.onclick=()=>{current=el.dataset.id;renderList();renderForm();});}
function renderForm(){
 focusPreview();
 const q=getCurrent();if(!q){$('form').innerHTML='<div class="empty"><h2>Comienza por una pregunta.</h2><p>Selecciona un elemento o crea uno nuevo.<br>Los contextos permiten usar una lectura, tabla o banco común una sola vez.</p></div>';return;}
 const english=q.area==='english',context=tab==='contexts';
 let html=`<div class="topline"><div><span class="eyebrow">${esc(areas[q.area])}</span><h2>${context?'Contexto compartido':'Editar pregunta'}</h2></div><button id="delete-item" class="danger">Eliminar</button></div>`;
 if(english)html+=select('Parte de inglés','part',{'1':'1 · Asociación de vocabulario','2':'2 · Avisos y señales','3':'3 · Conversaciones','4':'4 · Texto con espacios (A–C)','5':'5 · Comprensión literal (A–C)','6':'6 · Comprensión inferencial (A–D)','7':'7 · Texto con espacios (A–D)'},q.part);
 if(context){
  html+=input('Título','title',q.title)+text('Encabezado del grupo · numeración automática','range_heading',q.range_heading||'')+'<div class="actions"><button data-heading-preset="text">Según el texto</button><button data-heading-preset="information">Según la información</button><button data-heading-preset="graph">Según la gráfica</button><button data-heading-preset="auto">Automático</button></div><p class="note">Escribe, por ejemplo: Responda las preguntas {{desde}} a {{hasta}} según el siguiente texto. No escribas números fijos; se actualizarán solos. Vacío = encabezado automático.</p>'+text('Instrucciones adicionales del ejercicio','instructions',q.instructions)+text('Lectura o texto compartido','text',q.text)+'<p class="note">Para espacios usa {{h1}}, {{h2}}, etc. Después asigna h1 o h2 a cada pregunta. El PDF coloca la numeración final automáticamente.</p>'+imageField(q,'main')+text('Tabla opcional · una fila por línea, separa las celdas con punto y coma','table',q.table)+text('Fuente o crédito del texto, tabla o imagen (opcional)','source',q.source);
  if(english&&q.part===1)html+=text('Banco común · siete palabras, una por línea (A–G)','words',(q.words||[]).join('\n'))+input('Ejemplo resuelto, por ejemplo: This fruit is red. — H. apple','example',q.example);
 }else{
  const contexts=Object.fromEntries(state.contexts.filter(c=>c.area===q.area&&(!english||c.part===q.part)).map(c=>[c.id,c.title||'Contexto sin título']));
  html+='<div class="grid">'+input('Tema','topic',q.topic)+input('Subtema','subtopic',q.subtopic)+input('Orden dentro del área / parte','order',q.order,'number')+select('Distribución','layout',{columns:'Dos columnas con separador',boxed:'Pregunta en recuadro',full:'Ancho completo en recuadro'},q.layout)+'</div>';
  html+=`<label><input type="checkbox" data-field="included" ${q.included?'checked':''}>Incluir en el cuadernillo de esta sesión</label>`+select('Contexto compartido (opcional)','context',contexts,q.context)+'<p class="note">Crea o modifica lecturas y bancos en la pestaña Contextos. Las preguntas de un contexto permanecen juntas.</p>'+text('Introducción antes de la imagen (opcional)','introduction',q.introduction||'')+imageField(q,'main')+text('Pregunta o descripción (debajo de la imagen, si tiene)','stem',q.stem)+'<p class="note">Orden impreso: número e introducción → imagen → pregunta → opciones. Separa manualmente la introducción si antes escribiste todo en un solo campo.</p>';
  html+='<div class="actions"><button id="create-linked-context">+ Crear y vincular lectura / contexto</button>'+(q.context?'<button id="edit-linked-context">Editar contexto vinculado</button>':'')+'</div>';
  if(english&&[4,7].includes(q.part))html+=input('Identificador del espacio, sin llaves (ej. h1)','slot',q.slot);
  const count=english&&q.part===1?0:english&&[2,3,4,5].includes(q.part)?3:4;
  resizeOptions(q,count);
  html+='<h3>'+(count?'Opciones de respuesta':'Respuesta del banco común A–G')+'</h3>';
  if(count)html+=q.options.map((o,i)=>`<div class="option">${text('Opción '+'ABCD'[i],'option-'+i,o.text)}${imageField(o,'option-'+i)}</div>`).join('');
  html+=select('Clave correcta · cuadernillo resuelto y profesor','correct',Object.fromEntries([...(count?'ABCD'.slice(0,count):'ABCDEFG')].map(c=>[c,c])),q.correct)+text('Explicación de la respuesta · al final del cuadernillo resuelto','explanation',q.explanation);
  html+='<details><summary>Clasificación por competencias</summary><p class="note">Clasificación editorial del equipo SaberPlus; no requiere un docente. El catálogo de evidencias es parcial. No equivale a una validación externa ni asigna puntajes o niveles oficiales.</p>'+assessmentForm(q)+'</details>';
 }
 $('form').innerHTML=html;
 $('form').querySelectorAll('[data-classify]').forEach(el=>el.onchange=()=>{setClassification(q,el.checked);changed();renderForm();});
 $('form').querySelectorAll('[data-heading-preset]').forEach(el=>el.onclick=()=>{const presets={text:'RESPONDA LAS PREGUNTAS {{desde}} A {{hasta}} SEGÚN EL SIGUIENTE TEXTO',information:'RESPONDA LAS PREGUNTAS {{desde}} A {{hasta}} DE ACUERDO CON LA SIGUIENTE INFORMACIÓN',graph:'RESPONDA LAS PREGUNTAS {{desde}} A {{hasta}} SEGÚN LA SIGUIENTE GRÁFICA',auto:''};q.range_heading=presets[el.dataset.headingPreset];changed();renderForm();});
 if(!context){
  $('create-linked-context').onclick=()=>{if(q.context&&!confirm('Esta pregunta ya tiene contexto. ¿Vincularla a uno nuevo? El anterior se conserva.'))return;const ctx={id:id('ctx'),area:q.area,part:q.part||0,title:'',range_heading:'',instructions:'',text:'',table:'',source:'',words:[],example:''};state.contexts.push(ctx);q.context=ctx.id;tab='contexts';current=ctx.id;changed();refresh();};
  if(q.context)$('edit-linked-context').onclick=()=>{tab='contexts';current=q.context;refresh();};
 }
 $('delete-item').onclick=()=>{if(!confirm('¿Eliminar este '+(context?'contexto':'ítem')+' del proyecto?'))return;if(context&&state.questions.some(item=>item.context===q.id))return status('No se puede eliminar: todavía hay preguntas vinculadas a este contexto.',true);state[tab]=state[tab].filter(item=>item.id!==q.id);current=null;changed();renderList();renderForm();};
 $('form').querySelectorAll('[data-field]').forEach(el=>el.oninput=()=>{const key=el.dataset.field;let value=el.type==='checkbox'?el.checked:el.value;if(key==='part'||key==='order')value=Number(value);if(key==='words')value=el.value.split('\n');if(key.startsWith('option-'))q.options[Number(key.split('-')[1])].text=value;else q[key]=value;if(key==='part'){if(!context){q.assessment=blank(q.area);q.context=null;q.correct='';}changed();renderForm();}else changed();if(['title','topic','stem','included','part','order'].includes(key))renderList();});
 $('form').querySelectorAll('[data-assessment]').forEach(el=>el.onchange=()=>{updateClassification(q,el.dataset.assessment,el.value);changed();renderForm();});
 $('form').querySelectorAll('[data-upload]').forEach(el=>el.onchange=async()=>{const file=el.files[0];if(!file)return;try{if(file.size>5*1024*1024)throw Error('Máximo 5 MiB por imagen.');status('Cargando imagen…');const data=await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result.split(',')[1]);reader.onerror=reject;reader.readAsDataURL(file);});const result=await api('upload',{data});const obj=el.dataset.upload==='main'?q:q.options[Number(el.dataset.upload.split('-')[1])];obj.image=result.path;changed();renderForm();}catch(err){status(err.message,true);}});
 $('form').querySelectorAll('[data-remove]').forEach(el=>el.onclick=()=>{const obj=el.dataset.remove==='main'?q:q.options[Number(el.dataset.remove.split('-')[1])];delete obj.image;changed();renderForm();});
}
function assessmentForm(q){const a=q.assessment,cat=catalog.areas[q.area];let h=`<label><input type="checkbox" data-classify ${a.status!=='unclassified'?'checked':''}>Añadir clasificación por competencia</label>`;if(a.status==='unclassified')return h;const sel=(label,key,values)=>`<label>${label}<select data-assessment="${key}">${optionList(values,a[key])}</select></label>`;h+=sel('Competencia','competency',cat.competencies);if(q.area!=='english'){const claims=Object.fromEntries((cat.competencies[a.competency]?.claims||[]).map(k=>[k,k+' · '+cat.claims[k].label]));h+=sel('Afirmación','claim',claims);const ev=cat.claims[a.claim]?.evidence||[];h+=sel('Evidencia disponible','evidence',Object.fromEntries(ev.map(k=>[k,k])));if(q.area==='science')h+=sel('Componente','component',cat.components);if(q.area==='reading')h+='<p class="note">Proceso de lectura: '+esc(cat.processes[a.process]?.label||'Se asigna según la afirmación')+'</p>';}
 h+=`<label>Justificación de la clasificación<textarea data-assessment="rationale">${esc(a.rationale)}</textarea></label>`;return h;}
async function save(){const version=editVersion;const result=await api('save',{project:structuredClone(state),revision:state.revision});state.revision=result.project.revision;dirty=version!==editVersion;status(dirty?'Se guardó la versión enviada. Hay cambios nuevos todavía sin guardar.':'Proyecto guardado en este equipo. '+result.warnings.join(' '));return result;}
async function action(fn){if(busy)return;busy=true;$('save').disabled=$('generate').disabled=true;try{await fn();}catch(err){status(err.message,true);}finally{busy=false;$('save').disabled=$('generate').disabled=false;}}
$('save').onclick=()=>action(save);
$('live-refresh').onclick=()=>schedulePreview(true);
$('live-auto').onchange=()=>{if($('live-auto').checked)schedulePreview(true);else{clearTimeout(liveTimer);liveVersion++;$('live-status').textContent='Actualización automática pausada.';}};
$('live-page').onchange=()=>showLivePage($('live-page').value);
$('live-prev').onclick=()=>showLivePage(livePage-1);
$('live-next').onclick=()=>showLivePage(livePage+1);
$('live-zoom').onchange=()=>{$('live-paper').style.width=$('live-zoom').value+'%';};
$('live-image').onerror=()=>{$('live-status').textContent='No se pudo cargar esta página. Pulsa Actualizar para regenerar la vista.';};
$('generate').onclick=()=>action(async()=>{invalidateOutputs();await save();if(dirty)throw Error('Hay cambios nuevos. Guarda de nuevo antes de generar los PDF.');const version=editVersion,revision=state.revision;status('Componiendo cuadernillo, resuelto y clave del profesor…');const result=await api('generate',{revision});if(version!==editVersion||revision!==state.revision){invalidateOutputs();throw Error('El contenido cambió durante la generación. Los archivos anteriores no incluyen esos cambios; vuelve a generar.');}$('results').hidden=false;$('student').href=result.student;$('solved').href=result.solved;$('teacher').href=result.teacher;$('output-view').value='student';$('preview').src=result.student;$('warnings').textContent=result.warnings.length?'Pendientes del borrador:\n'+result.warnings.join('\n'):'Distribución configurada y clasificaciones registradas. Esto no sustituye una validación psicométrica ni externa.';status('Los 3 PDF están listos: '+result.questions+' preguntas. Revisa todas las páginas antes de imprimir.');$('results').scrollIntoView({behavior:'smooth'});});
$('output-view').onchange=()=>{$('preview').src=$($('output-view').value).href;};
['code','time'].forEach(key=>$(key).oninput=()=>{state[key]=$(key).value;changed();});
$('heading-area').onchange=renderAreaHeader;
['title','instructions'].forEach(key=>$('area-'+key).oninput=()=>{const chosen=$('heading-area').value;state.area_headers??={};state.area_headers[chosen]??={};state.area_headers[chosen][key]=$('area-'+key).value;changed();});
$('session').onchange=()=>{state.session=$('session').value;changed();refresh();};
$('area').onchange=()=>{area=$('area').value;current=null;renderList();renderForm();};
['questions','contexts'].forEach(t=>$(t+'-tab').onclick=()=>{tab=t;current=null;refresh();});
$('add').onclick=()=>{const q={id:id(tab==='questions'?'q':'ctx'),area,part:area==='english'?1:0};if(tab==='questions')Object.assign(q,{order:state.questions.length+1,topic:'',subtopic:'',stem:'',options:Array.from({length:4},()=>({text:''})),correct:'',explanation:'',layout:'columns',included:true,context:null,slot:'',assessment:blank(area)});else Object.assign(q,{title:'',instructions:'',text:'',table:'',words:[],example:''});state[tab].push(q);current=q.id;changed();renderList();renderForm();};
$('export').onclick=()=>{const blob=new Blob([JSON.stringify(state,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=state.code+'-proyecto.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
$('import').onchange=()=>action(async()=>{const file=$('import').files[0];if(!file)return;if(!confirm('¿Reemplazar el proyecto actual con este JSON? Descarga antes un respaldo si hay cambios sin guardar.'))return;const imported=JSON.parse(await file.text());const result=await api('save',{project:imported,revision:state.revision});state=result.project;editVersion++;invalidateOutputs();current=null;dirty=false;refresh();status('Proyecto importado y guardado.');});
$('demo').onclick=()=>action(async()=>{if(!confirm('¿Reemplazar el proyecto con 22 preguntas de muestra? Descarga antes tu JSON si tienes cambios sin guardar.'))return;const result=await api('demo',{revision:state.revision});state=result.project;editVersion++;invalidateOutputs();current=null;dirty=false;refresh();status('Muestra cargada. Primera sesión incluye 10 preguntas; cambia a segunda sesión para ver las partes de inglés. No es un simulacro completo ni validado.');});
window.addEventListener('beforeunload',event=>{if(dirty){event.preventDefault();event.returnValue='';}});
fetch('/api/bootstrap').then(r=>r.json()).then(data=>{({catalog,areas,sessions,token}=data);state=data.project;refresh();status('Proyecto local listo. Crea una pregunta o carga la demostración para probar la distribución.');}).catch(err=>status('No se pudo conectar: '+err.message,true));
