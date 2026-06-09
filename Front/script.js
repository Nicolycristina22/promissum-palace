const API = "http://localhost:5000";

const QUARTOS_LOCAL = [
  { id:"q-001", num:101, tipo:"STANDARD", tLabel:"Standard", nome:"Quarto Standard",
    preco:350, emoji:"🛏️", bg:"linear-gradient(135deg,#1e1a14,#2a2318)",
    desc:"Confortável e elegante, ideal para estadias de negócios ou viagens solo.",
    am:["Wi-Fi","TV HD","Ar-condicionado","Frigobar","Cofre"],
    capacidade:2, andar:1, temVaranda:false, temBanheira:false, areaM2:25 },
  { id:"q-002", num:202, tipo:"LUXO", tLabel:"Luxo", nome:"Quarto Luxo",
    preco:650, emoji:"🛋️", bg:"linear-gradient(135deg,#1a1808,#2b2510)",
    desc:"Amplo e sofisticado com decoração refinada e vista privilegiada da cidade.",
    am:["Wi-Fi Fibra","Smart TV 55\"","Banheira","Varanda","Room Service","Minibar"],
    capacidade:2, andar:2, temVaranda:true, temBanheira:true, areaM2:45 },
  { id:"q-003", num:301, tipo:"SUITE", tLabel:"Suíte", nome:"Suíte Presidencial",
    preco:1200, emoji:"👑", bg:"linear-gradient(135deg,#1a1608,#28220a)",
    desc:"Sala de estar separada, jacuzzi privativa e mordomia exclusiva 24 horas.",
    am:["Wi-Fi Dedicado","Home Theater","Jacuzzi","Sala de Estar","Mordomia 24h","Champagne"],
    capacidade:4, andar:3, temVaranda:true, temBanheira:true, areaM2:90 },
];

const QUARTO_POR_NUM = {};
QUARTOS_LOCAL.forEach(q => { QUARTO_POR_NUM[q.num] = q; });

const MESES = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
               "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"];

let usuarios = [], reservas = [], logado = null, qsel = null;
let filtroAtual = "todos", termoBusca = "";
let calA = new Date().getFullYear(), calM = new Date().getMonth();
let editCalA = calA, editCalM = calM, editQsel = null;
let quartosDB = {};

// Utilitários DOM ──────────────────
const eid = id => document.getElementById(id);
const g   = id => eid(id) ? eid(id).value.trim() : "";
const on  = (id, ev, fn) => { const el = eid(id); if (el) el.addEventListener(ev, fn); };
const sAl = (el, tipo, msg) => { el.className = "alert " + tipo; el.textContent = msg; };
const fd  = s => { const [y,m,d] = s.split("-"); return `${d}/${m}/${y}`; };
const inic  = n => n.split(" ").slice(0,2).map(x=>x[0]).join("").toUpperCase();
const pNome = n => n.split(" ")[0];
const lRole = r => r==="gerente"?"Gerente":r==="funcionario"?"Funcionário":"Hóspede";
const isStaff = () => logado && (logado.role==="gerente"||logado.role==="funcionario");

function fecharModal(id) { eid(id).classList.remove("open"); }
function togDrop()       { eid("drop").classList.toggle("open"); }
function ir(id)          { eid(id).scrollIntoView({ behavior:"smooth" }); }

function erroInput(id, msg) {
  const el = eid(id); if (!el) return;
  el.classList.add("input-err");
  const lb = el.closest(".fg")?.querySelector("label");
  if (lb) { lb.dataset.orig = lb.dataset.orig||lb.textContent; lb.textContent="⚠ "+msg; lb.classList.add("label-err"); }
  el.addEventListener("input", ()=>limparErro(id), { once:true });
}
function limparErro(id) {
  const el = eid(id); if (!el) return;
  el.classList.remove("input-err");
  const lb = el.closest(".fg")?.querySelector("label");
  if (lb&&lb.dataset.orig) { lb.textContent=lb.dataset.orig; lb.classList.remove("label-err"); delete lb.dataset.orig; }
}
const limparErros = ids => ids.forEach(limparErro);

// Init 
document.addEventListener("DOMContentLoaded", () => {
  const hoje = new Date().toISOString().split("T")[0];
  ["s-ci","s-co","r-ci","r-co"].forEach(id => { const e=eid(id); if(e) e.min=hoje; });

  on("btn-topo","click",()=>scrollTo(0,0));
  on("nav-quartos","click",()=>ir("sec-quartos"));
  on("nav-reservas","click",()=>ir("sec-reservas"));
  on("btn-ham","click",togDrop);
  on("nav-pill","click",togDrop);
  document.addEventListener("click", e => {
    if (!e.target.closest("#drop")&&!e.target.closest("#btn-ham")&&!e.target.closest("#nav-pill"))
      eid("drop").classList.remove("open");
  });

  on("btn-drop-login","click",()=>abrirLogin("login"));
  on("btn-drop-cad","click",()=>abrirLogin("cad"));
  on("btn-perfil","click",abrirPerfil);
  on("btn-minhas-res","click",()=>{ eid("drop").classList.remove("open"); ir("sec-reservas"); });
  on("btn-logout","click",logout);

  on("btn-fechar-login","click",()=>fecharModal("ov-login"));
  on("tb-l","click",()=>swTab("login")); on("tb-c","click",()=>swTab("cad"));
  on("btn-login","click",fazerLogin);    on("btn-cadastrar","click",cadastrar);
  ["l-email","l-pw"].forEach(id=>on(id,"keydown",e=>{ if(e.key==="Enter") fazerLogin(); }));

  on("btn-fechar-perfil","click",()=>fecharModal("ov-perfil"));
  on("btn-salvar-perfil","click",salvarPerfil);

  on("btn-fechar-res","click",()=>fecharModal("ov-res"));
  on("btn-noauth-login","click",()=>{ fecharModal("ov-res"); abrirLogin("login"); });
  on("btn-noauth-cad","click",()=>{ fecharModal("ov-res"); abrirLogin("cad"); });
  on("r-hsel","change",selHosp);
  on("r-ci","change",()=>{ atualizarTot(); renderCal(); });
  on("r-co","change",()=>{ atualizarTot(); renderCal(); });
  document.addEventListener("change", e => {
    if (e.target.classList.contains("svc-check")) atualizarTotComServicos();
    if (e.target.classList.contains("edit-svc-check")) atualizarTotEditComServicos();
  });  on("cal-prev","click",()=>calNav(-1)); on("cal-next","click",()=>calNav(1));
  on("btn-confirmar","click",confirmar);
  on("btn-filtrar","click",filtrar);
  on("fb-todos","click",function(){ setFilt("todos",this); });
  on("fb-ativo","click",function(){ setFilt("ATIVO",this); });
  on("fb-cancelado","click",function(){ setFilt("CANCELADO",this); });

  on("btn-fechar-edit-res","click",()=>fecharModal("ov-edit-res"));
  on("btn-salvar-edit-res","click",salvarEdicaoReserva);
  on("edit-ci","change",()=>{ atualizarTotEdit(); renderCalEdit(); });
  on("edit-co","change",()=>{ atualizarTotEdit(); renderCalEdit(); });
  on("edit-quarto","change",()=>{ atualizarTotEdit(); renderCalEdit(); });
  on("edit-cal-prev","click",()=>editCalNav(-1)); on("edit-cal-next","click",()=>editCalNav(1));

  on("btn-fechar-edit-cli","click",()=>fecharModal("ov-edit-cli"));
  on("btn-salvar-edit-cli","click",salvarEdicaoCliente);

  document.querySelectorAll(".overlay").forEach(o=>{
    o.addEventListener("click",e=>{ if(e.target===o) o.classList.remove("open"); });
  });

  carregarHospedes();
  renderQ(QUARTOS_LOCAL);
  renderP();
});

// Autenticação 
function abrirLogin(aba) { eid("drop").classList.remove("open"); swTab(aba); eid("ov-login").classList.add("open"); }
function swTab(t) {
  eid("tb-l").classList.toggle("active",t==="login");
  eid("tb-c").classList.toggle("active",t==="cad");
  eid("tp-login").style.display = t==="login"?"block":"none";
  eid("tp-cad").style.display   = t==="cad"?"block":"none";
}

async function fazerLogin() {
  const al=eid("al-login"), em=g("l-email"), pw=g("l-pw");
  limparErros(["l-email","l-pw"]);
  if (!em) { erroInput("l-email","Obrigatório"); return sAl(al,"err","Preencha todos os campos."); }
  if (!pw) { erroInput("l-pw","Obrigatório");    return sAl(al,"err","Preencha todos os campos."); }
  try {
    const resp = await fetch(`${API}/login`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:em,senha:pw})});
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.erro);
    entrar(data); fecharModal("ov-login");
  } catch(e) { sAl(al,"err","Credenciais inválidas. Verifique e-mail e senha."); }
}

async function cadastrar() {
  const al=eid("al-cad");
  const campos=["c-nome","c-doc","c-nasc","c-email","c-tel","c-end","c-cidade","c-estado","c-cep","c-nac","c-pw","c-pw2"];
  limparErros(campos);
  const pw=g("c-pw"), pw2=g("c-pw2");
  if (pw.length<4)  { erroInput("c-pw","Mínimo 4 caracteres"); return sAl(al,"err","Corrija os campos."); }
  if (pw!==pw2)     { erroInput("c-pw2","Senhas não coincidem"); return sAl(al,"err","Corrija os campos."); }
  const [dd,mm,aaaa] = g("c-nasc").split("/");
  const hospede = { nome:g("c-nome"), documento:g("c-doc"), email:g("c-email"), telefone:g("c-tel"),
    endereco:g("c-end"), cidade:g("c-cidade"), estado:g("c-estado"), cep:g("c-cep"),
    nacionalidade:g("c-nac"), data_nascimento:`${aaaa}-${mm}-${dd}`, senha:pw };
  const val = await fetch(`${API}/validar/hospede`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(hospede)});
  const vd  = await val.json();
  if (!val.ok) return sAl(al,"err",(vd.erros||["Erro de validação"]).join(" | "));
  try {
    const resp = await fetch(`${API}/hospedes`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(hospede)});
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.erro||"Erro ao cadastrar");
    entrar({id:data.id,nome:hospede.nome,documento:hospede.documento,email:hospede.email,role:"hospede",
            telefone:hospede.telefone,endereco:hospede.endereco,cidade:hospede.cidade,estado:hospede.estado,
            cep:hospede.cep,nacionalidade:hospede.nacionalidade,data_nascimento:hospede.data_nascimento});
    fecharModal("ov-login");
  } catch(e) { sAl(al,"err","Erro ao cadastrar: "+e.message); }
}

function entrar(u) {
  logado=u;
  eid("nav-pill").style.display="flex";
  eid("nav-av").textContent=inic(u.nome); eid("nav-nm").textContent=pNome(u.nome); eid("nav-rl").textContent=lRole(u.role);
  eid("drop-guest").style.display="none"; eid("drop-logged").style.display="block";
  eid("drop-av").textContent=inic(u.nome); eid("drop-nm").textContent=u.nome;
  eid("drop-rl").textContent=lRole(u.role); eid("drop-em").textContent=u.email;
  renderQ(QUARTOS_LOCAL); carregarReservas();
}

function logout() {
  logado=null;
  eid("nav-pill").style.display="none";
  eid("drop-guest").style.display="block"; eid("drop-logged").style.display="none";
  eid("drop").classList.remove("open");
  renderQ(QUARTOS_LOCAL); renderP();
}

// Perfil 
function abrirPerfil() {
  eid("drop").classList.remove("open"); if (!logado) return;
  eid("pf-nome").textContent=logado.nome; eid("pf-doc").textContent=logado.documento;
  eid("pf-email").textContent=logado.email; eid("pf-tel").textContent=logado.telefone||"—";
  eid("pf-end").textContent=logado.endereco||"—";
  eid("pf-cidade").textContent=(logado.cidade&&logado.estado)?`${logado.cidade} - ${logado.estado}`:"—";
  eid("pf-cep").textContent=logado.cep||"—"; eid("pf-nac").textContent=logado.nacionalidade||"—";
  eid("pf-nasc").textContent=logado.data_nascimento||"—";
  eid("al-pf").className="alert"; limparErros(["pf-edit-email","pf-edit-tel","pf-edit-end"]);
  eid("ov-perfil").classList.add("open");
}

async function salvarPerfil() {
  const al=eid("al-pf"), email=g("pf-edit-email"), tel=g("pf-edit-tel"), end=g("pf-edit-end");
  try {
    const resp = await fetch(`${API}/hospedes/${logado.id}`,{method:"PUT",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({email:email||logado.email,telefone:tel||logado.telefone,endereco:end||logado.endereco})});
    if (!resp.ok) throw new Error("Erro ao salvar");
    if (email) logado.email=email; if (tel) logado.telefone=tel; if (end) logado.endereco=end;
    sAl(al,"ok","✓ Dados atualizados!"); eid("drop-em").textContent=logado.email;
    setTimeout(()=>abrirPerfil(),700);
  } catch(e) { sAl(al,"err","Erro ao salvar: "+e.message); }
}

// Quartos 
function renderQ(lista) {
  const gr=eid("qgrid");
  if (!lista.length) { gr.innerHTML='<div class="es">Nenhum quarto disponível.</div>'; return; }
  gr.innerHTML = lista.map(q => {
    const ocu=isOcu(q.id), extras=[];
    if (q.temVaranda)  extras.push("🌅 Varanda");
    if (q.temBanheira) extras.push("🛁 Banheira");
    return `<div class="qcard">
      <div class="qimg" style="background:${q.bg}"><span>${q.emoji}</span><div class="qtbadge">${q.tLabel}</div></div>
      <div class="qbody">
        <div class="qnum">Quarto Nº ${q.num} · Andar ${q.andar} · ${q.areaM2}m²</div>
        <div class="qnom">${q.nome}</div><div class="qdesc">${q.desc}</div>
        <div class="qamen">${q.am.map(a=>`<span class="am">${a}</span>`).join("")}${extras.map(e=>`<span class="am am-dest">${e}</span>`).join("")}</div>
        <div class="q-cap">👥 Capacidade: ${q.capacidade} pessoa${q.capacidade>1?"s":""}</div>
        <div class="qfooter">
          <div class="qprice"><div class="val">R$ ${q.preco.toLocaleString("pt-BR")}</div><div class="per">por noite</div></div>
          <button class="btn-res${ocu?" btn-res-ocu":""}" data-qid="${q.id}" ${ocu?"disabled":""}>${ocu?"Indisponível":"Reservar"}</button>
        </div>
      </div></div>`;
  }).join("");
  gr.querySelectorAll(".btn-res:not([disabled])").forEach(btn=>btn.addEventListener("click",()=>abrirRes(btn.dataset.qid)));
}

function isOcu(qid) {
  const ci=eid("s-ci").value, co=eid("s-co").value; if (!ci||!co) return false;
  return reservas.some(r=>r.qid===qid&&r.st==="ATIVO"&&new Date(ci)<new Date(r.co)&&new Date(co)>new Date(r.ci));
}
function filtrar() { const t=eid("s-tipo").value; renderQ(t?QUARTOS_LOCAL.filter(q=>q.tipo===t):[...QUARTOS_LOCAL]); ir("sec-quartos"); }


async function carregarReservas() {
  try {
    const dados = await fetch(`${API}/reservas`).then(r=>r.json());
    reservas = dados.map(r => {
      const qL=QUARTO_POR_NUM[r.quarto_numero];
      return { id:r.id, hId:r.hospede_id, hNome:r.hospede_nome,
               qid:qL?qL.id:null, qNome:qL?qL.nome:`Quarto ${r.quarto_numero}`,
               qNum:r.quarto_numero, ci:r.check_in, co:r.check_out,
               st:r.status==="Ativo"?"ATIVO":"CANCELADO", tot:Number(r.valor_total),
               servicos:r.servicos_extras||[] };
    });
    dados.forEach(r=>{
      const idx=usuarios.findIndex(u=>u.id===r.hospede_id);
      const fresco={id:r.hospede_id,nome:r.hospede_nome,role:"hospede",
        email:r.hospede_email||"",telefone:r.hospede_telefone||"",
        documento:r.hospede_documento||"",endereco:r.hospede_endereco||"",
        cidade:r.hospede_cidade||"",estado:r.hospede_estado||"",
        cep:r.hospede_cep||"",nacionalidade:r.hospede_nacionalidade||"",
        data_nascimento:r.hospede_data_nascimento||""};
      if(idx>=0) usuarios[idx]={...usuarios[idx],...fresco};
      else usuarios.push(fresco);
    });
    renderQ(QUARTOS_LOCAL); renderP();
  } catch(e) { console.error("Erro ao carregar reservas:",e); renderP(); }
}

async function carregarHospedes() {
  try {
    const dados = await fetch(`${API}/hospedes`).then(r=>r.json());
    dados.forEach(h=>{ if(!usuarios.find(u=>u.id===h.id))
      usuarios.push({id:h.id,nome:h.nome,documento:h.documento,email:h.email,
        telefone:h.telefone,endereco:h.endereco,cidade:h.cidade,estado:h.estado,
        cep:h.cep,nacionalidade:h.nacionalidade,data_nascimento:h.data_nascimento,role:"hospede"});
    });
  } catch(e) { console.error("Erro ao carregar hóspedes:",e); }
}

async function getQuartoDBId(numQuarto) {
  if (quartosDB[numQuarto]) return quartosDB[numQuarto];
  const lista = await fetch(`${API}/quartos`).then(r=>r.json()).catch(()=>[]);
  lista.forEach(q=>{ quartosDB[q.numero]=q.id; });
  return quartosDB[numQuarto]||null;
}

// Reservar 
function abrirRes(qid) {
  qsel=QUARTOS_LOCAL.find(q=>q.id===qid);
  eid("res-qnome").textContent=qsel.nome;
  eid("res-qdet").textContent=`Andar ${qsel.andar} · ${qsel.areaM2}m² · Cap. ${qsel.capacidade} pessoa${qsel.capacidade>1?"s":""}`;
  eid("al-res").className="alert"; eid("r-tot").textContent=""; eid("r-tot-servicos").textContent="";
  document.querySelectorAll(".svc-check").forEach(c=>c.checked=false);
  const auth=!!logado;
  eid("bl-noauth").style.display=auth?"none":"block";
  eid("bl-auth").style.display=auth?"block":"none";
  if (auth) {
    const staff=isStaff();
    eid("bl-staff").style.display=staff?"block":"none";
    eid("bl-hospinfo").style.display=staff?"none":"block";
    if (staff) {
      const sel=eid("r-hsel");
      sel.innerHTML='<option value="">— Selecione —</option>'+
        usuarios.filter(u=>u.role==="hospede").map(u=>`<option value="${u.id}">${u.nome} (${u.documento||""})</option>`).join("");
      ["r-nnome","r-ndoc","r-nemail","r-ntel","r-nend","r-ncidade","r-nestado","r-ncep","r-nnac","r-nnasc"]
        .forEach(id=>{ if(eid(id)){eid(id).value="";limparErro(id);} });
    } else {
      eid("r-nome").value=logado.nome; eid("r-doc2").value=logado.documento;
      eid("r-email2").value=logado.email; eid("r-tel2").value=logado.telefone||"";
    }
    const ci=eid("s-ci").value, co=eid("s-co").value;
    if (ci) eid("r-ci").value=ci; if (co) eid("r-co").value=co;
    atualizarTot();
    const d=ci?new Date(ci+"T12:00:00"):new Date();
    calA=d.getFullYear(); calM=d.getMonth(); renderCal();
  }
  eid("ov-res").classList.add("open");
}

function selHosp() {
  if (eid("r-hsel").value)
    ["r-nnome","r-ndoc","r-nemail","r-ntel","r-nend","r-ncidade","r-nestado","r-ncep","r-nnac","r-nnasc"]
      .forEach(id=>{ if(eid(id)){eid(id).value="";limparErro(id);} });
}

async function atualizarTot() {
  if (!qsel) return;
  const ci=eid("r-ci").value, co=eid("r-co").value, el=eid("r-tot");
  if (!ci||!co) { el.textContent=""; eid("r-tot-servicos").textContent=""; return; }
  const resp=await fetch(`${API}/calcular/diarias`,{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({check_in:ci,check_out:co,preco_noite:qsel.preco})}).then(r=>r.json()).catch(()=>({}));
  el.textContent=resp.noites?`${resp.noites} noite(s) · Hospedagem: R$ ${resp.total.toLocaleString("pt-BR")}`:"";
  atualizarTotComServicos();
}

function getServicosSelecionados() {
  return [...document.querySelectorAll(".svc-check:checked")].map(c=>c.value);
}

function atualizarTotComServicos() {
  if (!qsel) return;
  const ci=eid("r-ci").value, co=eid("r-co").value;
  const el=eid("r-tot-servicos"); if (!el) return;
  if (!ci||!co) { el.textContent=""; return; }
  const noites=Math.round((new Date(co)-new Date(ci))/86400000); if (noites<=0){el.textContent="";return;}
  const PRECOS={"cafe_da_manha":50,"estacionamento":30,"late_checkout":80,"transfer_aeroporto":120};
  const NOMES={"cafe_da_manha":"Café da manhã","estacionamento":"Estacionamento","late_checkout":"Late check-out","transfer_aeroporto":"Transfer aeroporto"};
  const sels=getServicosSelecionados();
  const extraBase=sels.reduce((s,k)=>s+(PRECOS[k]||0),0);
  const extraTotal=sels.reduce((s,k)=>{
    if (k==="cafe_da_manha"||k==="estacionamento") return s+(PRECOS[k]*noites);
    return s+(PRECOS[k]||0);
  },0);
  const hospedagem=noites*qsel.preco;
  const total=hospedagem+extraTotal;
  if (!sels.length) { el.textContent=""; return; }
  const desc=sels.map(k=>NOMES[k]).join(", ");
  el.textContent=`Serviços: ${desc} · Total geral: R$ ${total.toLocaleString("pt-BR")}`;
}

function calNav(d)  { calM+=d; if(calM>11){calM=0;calA++;}if(calM<0){calM=11;calA--;}renderCal(); }
function renderCal() { _renderCalendario("cal-tit","cal-g",eid("r-ci").value,eid("r-co").value,qsel,calA,calM,null); }

async function confirmar() {
  const al=eid("al-res"), ci=eid("r-ci").value, co=eid("r-co").value;
  limparErros(["r-ci","r-co"]);
  if (!ci){erroInput("r-ci","Selecione a data");} if (!co){erroInput("r-co","Selecione a data");}
  if (!ci||!co) return sAl(al,"err","Informe as datas.");

  let hospedeId;
  if (isStaff()) {
    const sid=eid("r-hsel").value;
    if (sid) {
      hospedeId=Number(sid); if (!hospedeId) return sAl(al,"err","Hóspede inválido.");
    } else {

      const [dd2,mm2,aaaa2]=g("r-nnasc").split("/");
      const quartoDBId=await getQuartoDBId(qsel.num);
      if (!quartoDBId) return sAl(al,"err","Quarto não encontrado no sistema.");
      try {
        const resp=await fetch(`${API}/reservas/com-hospede`,{method:"POST",headers:{"Content-Type":"application/json"},
          body:JSON.stringify({hospede:{nome:g("r-nnome"),documento:g("r-ndoc"),email:g("r-nemail"),
            telefone:g("r-ntel"),endereco:g("r-nend"),cidade:g("r-ncidade"),estado:g("r-nestado"),
            cep:g("r-ncep"),nacionalidade:g("r-nnac"),data_nascimento:`${aaaa2}-${mm2}-${dd2}`},
            quarto_id:quartoDBId,check_in:ci,check_out:co,
            observacao:g("r-obs"),forma_pagamento:g("r-pgto")||"PIX"})});
        const data=await resp.json();
        if (!resp.ok) return sAl(al,"err",(data.erros||[data.erro]).join(" | "));
        await carregarReservas(); sAl(al,"ok","✓ Reserva confirmada!"); setTimeout(()=>fecharModal("ov-res"),1200); return;
      } catch(e) { return sAl(al,"err","Erro: "+e.message); }
    }
  } else {
    const hid = logado.hospede_id || logado.id;
    if (typeof hid!=="number") return sAl(al,"err","Conta não cadastrada no sistema.");
    hospedeId=hid;
  }

  const quartoDBId=await getQuartoDBId(qsel.num);
  if (!quartoDBId) return sAl(al,"err","Quarto não encontrado no sistema.");
  try {
    const resp=await fetch(`${API}/reservas`,{method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({hospede_id:hospedeId,quarto_id:quartoDBId,check_in:ci,check_out:co,
        observacao:g("r-obs")||"",forma_pagamento:g("r-pgto")||"PIX",
        servicos_extras:getServicosSelecionados()})});
    const data=await resp.json();
    if (!resp.ok) throw new Error(data.erro||"Erro ao salvar reserva");
    await carregarReservas(); sAl(al,"ok",`✓ Reserva confirmada! ${fd(ci)} → ${fd(co)}`);
    setTimeout(()=>fecharModal("ov-res"),1200);
  } catch(e) { sAl(al,"err","Erro: "+e.message); }
}

// Painel de Reservas
function setFilt(f,btn) { filtroAtual=f; document.querySelectorAll(".fb").forEach(x=>x.classList.remove("active")); btn.classList.add("active"); renderListaReservas(); }
function buscarNoPainel() { termoBusca=(eid("painel-busca")?.value||"").trim().toLowerCase(); renderListaReservas(); }
function limparBuscaPainel() { termoBusca=""; const el=eid("painel-busca"); if(el) el.value=""; renderListaReservas(); }

function renderP() {
  const eT=eid("ptit"),eS=eid("psub"),eF=eid("pfilt"),eSt=eid("pstats"),eL=eid("plista");
  if (!logado) {
    eT.textContent="Área Restrita"; eS.textContent="Faça login para ver suas reservas";
    eF.style.display=eSt.style.display="none";
    const bw=eid("painel-busca-wrap"); if(bw) bw.style.display="none";
    eL.innerHTML=`<div class="pl"><div class="li">🔒</div><div class="lt"><a id="pl-login" href="#">Faça login</a> ou <a id="pl-cad" href="#">crie uma conta</a> para visualizar suas reservas.</div></div>`;
    eid("pl-login")?.addEventListener("click",e=>{e.preventDefault();abrirLogin("login");});
    eid("pl-cad")?.addEventListener("click",e=>{e.preventDefault();abrirLogin("cad");});
    return;
  }
  const staff=isStaff();
  if (staff) {
    eT.textContent=logado.role==="gerente"?"Painel Gerencial":"Painel de Reservas";
    eS.textContent=logado.role==="gerente"?"Todas as reservas do hotel":"Gerenciamento de reservas";
    eF.style.display="flex";
    if (!eid("painel-busca-wrap")) {
      const barra=document.createElement("div"); barra.id="painel-busca-wrap";
      barra.style.cssText="margin-bottom:18px;display:flex;gap:8px;align-items:center";
      barra.innerHTML=`<input id="painel-busca" type="text" class="painel-busca-input" placeholder="Buscar por nome, CPF ou nº do quarto..."/>
        <button id="btn-limpar-busca" class="btn-limpar-busca">Limpar</button>`;
      eSt.parentNode.insertBefore(barra,eSt);
      on("painel-busca","input",buscarNoPainel); on("btn-limpar-busca","click",limparBuscaPainel);
    }
    eid("painel-busca-wrap").style.display="flex";
    if (logado.role==="gerente") {
      eSt.style.display="grid";
      const at=reservas.filter(r=>r.st==="ATIVO").length, ca=reservas.filter(r=>r.st==="CANCELADO").length;
      const re=reservas.filter(r=>r.st==="ATIVO").reduce((s,r)=>s+r.tot,0);
      eSt.innerHTML=`<div class="sc"><div class="sl">Total</div><div class="sv">${reservas.length}</div></div>
        <div class="sc"><div class="sl">Ativas</div><div class="sv">${at}</div></div>
        <div class="sc"><div class="sl">Canceladas</div><div class="sv">${ca}</div></div>
        <div class="sc"><div class="sl">Receita</div><div class="sv" style="font-size:20px">R$ ${re.toLocaleString("pt-BR")}</div></div>`;
    } else { eSt.style.display="none"; }
    renderListaReservas();
  } else {
    eT.textContent="Minhas Reservas"; eS.textContent="Olá, "+pNome(logado.nome);
    eF.style.display=eSt.style.display="none";
    const bw=eid("painel-busca-wrap"); if(bw) bw.style.display="none";
    const meuId=logado.hospede_id||logado.id;
    const lista=reservas.filter(r=>r.hId===meuId);
    eL.innerHTML=lista.length?lista.map(r=>iRes(r,"",true,false)).join(""):'<div class="es">Você ainda não possui reservas.</div>';
    registrarBotoes();
  }
}

function renderListaReservas() {
  const eL=eid("plista");
  let lista=[...reservas];
  if (filtroAtual!=="todos") lista=lista.filter(r=>r.st===filtroAtual);
  if (termoBusca) {
    const tb=termoBusca.replace(/\D/g,"");
    lista=lista.filter(r=>{ const u=usuarios.find(u=>u.id===r.hId),doc=(u?.documento||"").replace(/\D/g,"");
      return r.hNome.toLowerCase().includes(termoBusca)||(tb&&doc&&doc.includes(tb))||String(r.qNum)===termoBusca; });
  }
  if (!lista.length) { eL.innerHTML=termoBusca?`<div class="es">Nenhuma reserva para <strong>"${termoBusca}"</strong>.</div>`:'<div class="es">Nenhuma reserva encontrada.</div>'; return; }
  eL.innerHTML=lista.map(r=>{ const u=usuarios.find(u=>u.id===r.hId),rb=u&&u.role!=="hospede"?`<span class="badge ${u.role==="gerente"?"bg2":"bf"}">${lRole(u.role)}</span>`:""; return iRes(r,rb,true); }).join("");
  registrarBotoes();
}

function iRes(r,xb,sv,showCli) {
  if(showCli===undefined) showCli=sv;
  const u=usuarios.find(u=>u.id===r.hId), pc=r.st==="ATIVO"&&(sv||r.hId===logado?.id);
  let ci="";
  if (showCli&&u) {
    const ls=[];
    if(u.email) ls.push(`📧 ${u.email}`); if(u.telefone) ls.push(`📱 ${u.telefone}`);
    if(u.documento) ls.push(`🪪 ${u.documento}`);
    if(u.endereco) ls.push(`📍 ${u.endereco}${u.cidade?", "+u.cidade:""}${u.estado?" - "+u.estado:""}${u.cep?" · CEP "+u.cep:""}`);
    if(u.nacionalidade) ls.push(`🌐 ${u.nacionalidade}`); if(u.data_nascimento) ls.push(`🎂 ${u.data_nascimento}`);
    if(ls.length) ci=`<div class="ri-cliente">${ls.map(l=>`<span>${l}</span>`).join("")}</div>`;
  }
  const NOMES_SVC={"cafe_da_manha":"☕ Café da manhã","estacionamento":"🚗 Estacionamento","late_checkout":"🕐 Late check-out","transfer_aeroporto":"✈️ Transfer aeroporto"};
  const svcs=(r.servicos||[]).map(s=>NOMES_SVC[s]||s).join(" · ");
  const svcsHtml=svcs?`<div class="ri-servicos">${svcs}</div>`:"";
  return `<div class="ri"><div class="ri-inf"><div class="ri-nome">${r.hNome} ${xb}</div>
    <div class="ri-det">${r.qNome} · Nº ${r.qNum}<span class="sep">|</span>${fd(r.ci)} → ${fd(r.co)}<span class="sep">|</span>R$ ${r.tot.toLocaleString("pt-BR")}</div>${svcsHtml}${ci}</div>
    <span class="badge ${r.st==="ATIVO"?"ba":"bc"}">${r.st==="ATIVO"?"Ativo":"Cancelado"}</span>
    ${pc?`<button class="btn-edit" data-rid="${r.id}">✏️ Editar</button>`:""}
    ${sv&&r.st==="ATIVO"?`<button class="btn-edit" data-hid="${r.hId}">👤 Editar cliente</button>`:""}
    ${pc?`<button class="btn-can" data-rid="${r.id}">Cancelar</button>`:""}</div>`;
}

function registrarBotoes() {
  document.querySelectorAll(".btn-can").forEach(b=>b.addEventListener("click",()=>cancelar(b.dataset.rid)));
  document.querySelectorAll(".btn-edit[data-rid]").forEach(b=>b.addEventListener("click",()=>abrirEditarReserva(b.dataset.rid)));
  document.querySelectorAll(".btn-edit[data-hid]").forEach(b=>b.addEventListener("click",()=>abrirEditarCliente(Number(b.dataset.hid))));
}

async function cancelar(rid) {
  const r=reservas.find(r=>r.id==rid); if(!r||r.st==="CANCELADO") return;
  const meuHid=logado.hospede_id||logado.id;
  if(logado.role==="hospede"&&r.hId!==meuHid) return;
  try { const resp=await fetch(`${API}/reservas/${rid}`,{method:"DELETE"});
    if(!resp.ok) throw new Error("Erro ao cancelar"); await carregarReservas(); }
  catch(e) { alert("Erro ao cancelar: "+e.message); }
}

// Editar Reserva 
function abrirEditarReserva(rid) {
  const r=reservas.find(r=>r.id==rid); if(!r) return;
  const sel=eid("edit-quarto");
  sel.innerHTML=QUARTOS_LOCAL.map(q=>`<option value="${q.id}">${q.nome} (Nº ${q.num}) — R$ ${q.preco.toLocaleString("pt-BR")}/noite</option>`).join("");
  const hoje=new Date().toISOString().split("T")[0];
  eid("edit-ci").min=eid("edit-co").min=hoje;
  eid("edit-ci").value=r.ci; eid("edit-co").value=r.co;
  sel.value=r.qid||QUARTOS_LOCAL[0].id;
  eid("al-edit-res").className="alert"; eid("al-edit-res").textContent="";
  editQsel=QUARTOS_LOCAL.find(q=>q.id===(r.qid||QUARTOS_LOCAL[0].id));
  const d=new Date(r.ci+"T12:00:00"); editCalA=d.getFullYear(); editCalM=d.getMonth();
  eid("ov-edit-res").dataset.rid=rid;
  document.querySelectorAll(".edit-svc-check").forEach(c=>{
    c.checked=(r.servicos||[]).includes(c.value);
  });
  atualizarTotEdit(); renderCalEdit();
  eid("ov-edit-res").classList.add("open");
}

function editCalNav(d) { editCalM+=d; if(editCalM>11){editCalM=0;editCalA++;}if(editCalM<0){editCalM=11;editCalA--;}renderCalEdit(); }
function renderCalEdit() {
  const qid=eid("edit-quarto")?.value; if(qid) editQsel=QUARTOS_LOCAL.find(q=>q.id===qid);
  if(!editQsel) return;
  _renderCalendario("edit-cal-tit","edit-cal-g",eid("edit-ci").value,eid("edit-co").value,editQsel,editCalA,editCalM,eid("ov-edit-res")?.dataset.rid);
}

async function atualizarTotEdit() {
  const ci=eid("edit-ci")?.value, co=eid("edit-co")?.value, qid=eid("edit-quarto")?.value, el=eid("edit-tot");
  if(!el) return; if(!ci||!co||!qid){el.textContent="";return;}
  const q=QUARTOS_LOCAL.find(q=>q.id===qid); if(!q){el.textContent="";return;}
  const resp=await fetch(`${API}/calcular/diarias`,{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({check_in:ci,check_out:co,preco_noite:q.preco})}).then(r=>r.json()).catch(()=>({}));
  el.textContent=resp.noites?`${resp.noites} noite(s) · Hospedagem: R$ ${resp.total.toLocaleString("pt-BR")}`:"";
  atualizarTotEditComServicos();
}

function atualizarTotEditComServicos() {
  const ci=eid("edit-ci")?.value, co=eid("edit-co")?.value, qid=eid("edit-quarto")?.value;
  const el=eid("edit-tot-servicos"); if(!el) return;
  if(!ci||!co||!qid){el.textContent="";return;}
  const noites=Math.round((new Date(co)-new Date(ci))/86400000); if(noites<=0){el.textContent="";return;}
  const PRECOS={"cafe_da_manha":50,"estacionamento":30,"late_checkout":80,"transfer_aeroporto":120};
  const NOMES={"cafe_da_manha":"Café da manhã","estacionamento":"Estacionamento","late_checkout":"Late check-out","transfer_aeroporto":"Transfer aeroporto"};
  const q=QUARTOS_LOCAL.find(q=>q.id===qid); if(!q){el.textContent="";return;}
  const sels=[...document.querySelectorAll(".edit-svc-check:checked")].map(c=>c.value);
  if(!sels.length){el.textContent="";return;}
  const extraTotal=sels.reduce((s,k)=>(k==="cafe_da_manha"||k==="estacionamento")?s+(PRECOS[k]*noites):s+(PRECOS[k]||0),0);
  const total=(noites*q.preco)+extraTotal;
  el.textContent=`Serviços: ${sels.map(k=>NOMES[k]).join(", ")} · Total geral: R$ ${total.toLocaleString("pt-BR")}`;
}

async function salvarEdicaoReserva() {
  const al=eid("al-edit-res"), rid=eid("ov-edit-res").dataset.rid;
  const ci=eid("edit-ci").value, co=eid("edit-co").value, qid=eid("edit-quarto").value;
  if(!ci||!co) return sAl(al,"err","Informe as datas.");
  const q=QUARTOS_LOCAL.find(q=>q.id===qid), quartoDBId=await getQuartoDBId(q.num);
  if(!quartoDBId) return sAl(al,"err","Quarto não encontrado no sistema.");
  try {
    const resp=await fetch(`${API}/reservas/${rid}`,{method:"PUT",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({quarto_id:quartoDBId,check_in:ci,check_out:co})});
    if(!resp.ok){const d=await resp.json().catch(()=>({}));throw new Error(d.erro||"Erro ao atualizar");}

    const svcs=[...document.querySelectorAll(".edit-svc-check:checked")].map(c=>c.value);
    const respSvcs=await fetch(`${API}/reservas/${rid}/servicos`,{method:"PUT",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({servicos:svcs})});

    if(!respSvcs.ok){const ds=await respSvcs.json().catch(()=>({}));throw new Error(ds.erro||"Erro ao salvar serviços");}
    const svcs2=[...document.querySelectorAll(".edit-svc-check:checked")].map(c=>c.value);
    const PRECOS2={"cafe_da_manha":50,"estacionamento":30,"late_checkout":80,"transfer_aeroporto":120};
    const noites2=Math.round((new Date(co)-new Date(ci))/86400000);
    const extraTotal2=svcs2.reduce((s,k)=>(k==="cafe_da_manha"||k==="estacionamento")?s+(PRECOS2[k]*noites2):s+(PRECOS2[k]||0),0);
    const novoTot=(noites2*q.preco)+extraTotal2;
    const ridx=reservas.findIndex(x=>x.id==rid);
    if(ridx>=0){ reservas[ridx]={...reservas[ridx],ci,co,qid:q.id,qNome:q.nome,qNum:q.num,tot:novoTot,servicos:svcs2}; }
    renderP(); sAl(al,"ok",`✓ Reserva atualizada! ${fd(ci)} → ${fd(co)}`);
    setTimeout(()=>fecharModal("ov-edit-res"),1400);
  } catch(e) { sAl(al,"err","Erro ao salvar: "+e.message); }
}

// Editar Cliente
function abrirEditarCliente(hid) {
  const u=usuarios.find(u=>u.id===hid); if(!u) return;
  ["nome","email","tel","end","cidade","estado","cep","nac"].forEach(k=>{
    const el=eid("ec-"+k); if(el) el.value=u[k==="tel"?"telefone":k==="end"?"endereco":k==="nac"?"nacionalidade":k]||"";
  });
  eid("al-edit-cli").className="alert"; eid("al-edit-cli").textContent="";
  eid("ov-edit-cli").dataset.hid=hid; eid("ov-edit-cli").classList.add("open");
}

async function salvarEdicaoCliente() {
  const al=eid("al-edit-cli"), hid=Number(eid("ov-edit-cli").dataset.hid);
  const nome=eid("ec-nome").value.trim(), email=eid("ec-email").value.trim();
  if(!nome) return sAl(al,"err","Nome é obrigatório.");
  const payload={nome,email,telefone:eid("ec-tel").value.trim(),endereco:eid("ec-end").value.trim(),
    cidade:eid("ec-cidade").value.trim(),estado:eid("ec-estado").value.trim(),
    cep:eid("ec-cep").value.trim(),nacionalidade:eid("ec-nac").value.trim()};
  try {
    const resp=await fetch(`${API}/hospedes/${hid}`,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
    if(!resp.ok){const d=await resp.json().catch(()=>({}));throw new Error(d.erro||"Erro ao atualizar");}
    const idx=usuarios.findIndex(u=>u.id===hid); if(idx>=0) usuarios[idx]={...usuarios[idx],...payload};
    renderP(); sAl(al,"ok","✓ Hóspede atualizado!"); setTimeout(()=>fecharModal("ov-edit-cli"),1400);
  } catch(e) { sAl(al,"err","Erro ao salvar: "+e.message); }
}

// Calendário
function _renderCalendario(titId, gridId, ci, co, quarto, ano, mes, ridIgnorar) {
  const titEl=eid(titId), gEl=eid(gridId); if(!titEl||!gEl||!quarto) return;
  titEl.textContent=MESES[mes]+" "+ano;
  const hoje=new Date(); hoje.setHours(0,0,0,0);
  const dias=["D","S","T","Q","Q","S","S"];
  let h=dias.map(d=>`<div class="cd">${d}</div>`).join("");
  const prim=new Date(ano,mes,1).getDay();
  for(let i=0;i<prim;i++) h+=`<div class="cy"></div>`;
  const tot=new Date(ano,mes+1,0).getDate();
  for(let d=1;d<=tot;d++){
    const dt=new Date(ano,mes,d); dt.setHours(0,0,0,0);
    const ocu=reservas.some(r=>(!ridIgnorar||r.id!=ridIgnorar)&&r.qid===quarto.id&&r.st==="ATIVO"&&new Date(r.ci+"T12:00:00")<=dt&&new Date(r.co+"T12:00:00")>dt);
    const hj=dt.getTime()===hoje.getTime();
    const sel=ci&&co&&new Date(ci+"T12:00:00")<=dt&&new Date(co+"T12:00:00")>dt;
    h+=`<div class="cy ${ocu?"occ":sel?"sel":hj?"tod":"free"}">${d}</div>`;
  }
  gEl.innerHTML=h;
}
