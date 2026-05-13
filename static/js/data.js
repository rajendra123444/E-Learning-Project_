/* ===== DATA ===== ===== CONSTANTS ===== */
const BRANCHES = [
  { code:'CSE',  name:'Computer Science' },
  { code:'IT',   name:'Information Technology' },
  { code:'ME',   name:'Mechanical' },
  { code:'CE',   name:'Civil' },
  { code:'EE',   name:'Electrical' },
  { code:'PHARMA', name:'Pharmacy' },
];

const SAMPLE_PDF = 'https://www.africau.edu/images/default/sample.pdf';

let notes = [
  { id:'n1', title:'Data Structures — Trees & Graphs', subject:'Data Structures', branch:'CSE', semester:3, unit:4, description:'Comprehensive notes covering binary trees, AVL, BST, graph traversals (BFS/DFS).', uploaded_by:'Aarav Mehta', uploaded_at:'2025-04-12', download_count:1284, tags:['trees','graphs','dsa'] },
  { id:'n2', title:'Operating Systems — Process Scheduling', subject:'Operating Systems', branch:'CSE', semester:4, unit:2, description:'FCFS, SJF, Round Robin, Priority scheduling with examples.', uploaded_by:'Priya Sharma', uploaded_at:'2025-03-22', download_count:942, tags:['os','scheduling'] },
  { id:'n3', title:'DBMS — Normalization (1NF–BCNF)', subject:'DBMS', branch:'IT', semester:4, unit:3, description:'Functional dependencies, decomposition, lossless joins.', uploaded_by:'You', uploaded_at:'2025-05-01', download_count:412, tags:['dbms','normalization'], mine:true },
  { id:'n4', title:'Thermodynamics — Laws & Cycles', subject:'Thermodynamics', branch:'ME', semester:3, unit:1, description:'First, second law, Carnot, Otto, Diesel cycles.', uploaded_by:'Rohit Verma', uploaded_at:'2025-02-18', download_count:730, tags:['thermo','mech'] },
  { id:'n5', title:'Computer Networks — OSI & TCP/IP', subject:'Networks', branch:'CSE', semester:5, unit:1, description:'Layered architectures, protocols at each layer.', uploaded_by:'You', uploaded_at:'2025-04-30', download_count:215, tags:['networks','osi'], mine:true },
  { id:'n6', title:'Pharmacology — Autonomic Drugs', subject:'Pharmacology', branch:'PHARMA', semester:4, unit:2, description:'Adrenergic & cholinergic agonists/antagonists.', uploaded_by:'Sneha Iyer', uploaded_at:'2025-01-10', download_count:510, tags:['pharma'] },
  { id:'n7', title:'Power Systems — Load Flow', subject:'Power Systems', branch:'EE', semester:6, unit:3, description:'Gauss-Seidel, Newton-Raphson methods.', uploaded_by:'Vikram Singh', uploaded_at:'2025-03-05', download_count:287, tags:['ee','power'] },
  { id:'n8', title:'Structural Analysis — Trusses', subject:'Structures', branch:'CE', semester:4, unit:2, description:'Method of joints, sections, virtual work.', uploaded_by:'Anita Rao', uploaded_at:'2025-02-25', download_count:360, tags:['ce','trusses'] },
];

let bookmarks = [];

let doubts = [
  { id:'d1', title:'Difference between BFS and DFS in real-world use?', description:'When should I use BFS vs DFS for a problem? Any rule of thumb?', subject:'Data Structures', branch:'CSE', semester:3, asked_by:'Aarav Mehta', asked_at:'2025-05-02', is_solved:true, views:132, replies:[
    { by:'Priya Sharma', answer:'BFS for shortest path on unweighted graphs, DFS for connectivity / topological sort / cycle detection.', is_best:true },
  ]},
  { id:'d2', title:'How does paging differ from segmentation?', description:'I keep mixing these up before exams. Can someone explain simply?', subject:'OS', branch:'CSE', semester:4, asked_by:'You', asked_at:'2025-05-04', is_solved:false, views:41, replies:[] },
  { id:'d3', title:'Carnot cycle efficiency derivation help', description:'Stuck on the derivation, mainly the entropy step.', subject:'Thermodynamics', branch:'ME', semester:3, asked_by:'Rohit Verma', asked_at:'2025-04-29', is_solved:false, views:88, replies:[] },
];

const books = [
  { id:'b1', title:'Let Us C', author:'Yashavant Kanetkar', subject:'Programming', branch:'CSE', semester:1, rating:5, cover_gradient:'linear-gradient(135deg,#6c63ff,#00d4ff)', description:'The classic introduction to C programming.' },
  { id:'b2', title:'Introduction to Algorithms', author:'CLRS', subject:'Algorithms', branch:'CSE', semester:4, rating:5, cover_gradient:'linear-gradient(135deg,#ff6b9d,#c44dff)', description:'The definitive algorithms textbook.' },
  { id:'b3', title:'Operating System Concepts', author:'Silberschatz', subject:'OS', branch:'CSE', semester:4, rating:4, cover_gradient:'linear-gradient(135deg,#00d4ff,#39ff14)', description:'The dinosaur book — OS fundamentals.' },
  { id:'b4', title:'Engineering Thermodynamics', author:'P.K. Nag', subject:'Thermo', branch:'ME', semester:3, rating:4, cover_gradient:'linear-gradient(135deg,#ff6b9d,#ffb86b)', description:'Standard reference for thermodynamics.' },
  { id:'b5', title:'Database System Concepts', author:'Korth & Silberschatz', subject:'DBMS', branch:'IT', semester:4, rating:5, cover_gradient:'linear-gradient(135deg,#6c63ff,#ff6b9d)', description:'Comprehensive DBMS textbook.' },
  { id:'b6', title:'Power System Analysis', author:'Hadi Saadat', subject:'Power', branch:'EE', semester:6, rating:4, cover_gradient:'linear-gradient(135deg,#39ff14,#00d4ff)', description:'Modern power systems engineering.' },
];

const pyqs = [
  { id:'p1', subject:'Data Structures', branch:'CSE', semester:3, year:2024, exam_type:'end' },
  { id:'p2', subject:'Data Structures', branch:'CSE', semester:3, year:2023, exam_type:'end' },
  { id:'p3', subject:'Operating Systems', branch:'CSE', semester:4, year:2024, exam_type:'mid' },
  { id:'p4', subject:'Operating Systems', branch:'CSE', semester:4, year:2022, exam_type:'end' },
  { id:'p5', subject:'DBMS', branch:'IT', semester:4, year:2023, exam_type:'end' },
  { id:'p6', subject:'Thermodynamics', branch:'ME', semester:3, year:2021, exam_type:'end' },
  { id:'p7', subject:'Networks', branch:'CSE', semester:5, year:2024, exam_type:'end' },
  { id:'p8', subject:'Pharmacology', branch:'PHARMA', semester:4, year:2020, exam_type:'back' },
];

const syllabi = [
  { id:'s1', subject_name:'Data Structures', subject_code:'CS301', branch:'CSE', semester:3, total_units:5, units:[
    {n:1,topic:'Arrays, Linked Lists, Stacks, Queues'},
    {n:2,topic:'Recursion & Searching/Sorting algorithms'},
    {n:3,topic:'Trees: BST, AVL, B-Trees'},
    {n:4,topic:'Graphs: Representation, BFS, DFS, MST, Shortest Paths'},
    {n:5,topic:'Hashing & Advanced data structures'},
  ]},
  { id:'s2', subject_name:'Operating Systems', subject_code:'CS401', branch:'CSE', semester:4, total_units:5, units:[
    {n:1,topic:'Introduction & Process Management'},
    {n:2,topic:'CPU Scheduling & Synchronization'},
    {n:3,topic:'Deadlocks & Memory Management'},
    {n:4,topic:'Virtual Memory & File Systems'},
    {n:5,topic:'I/O Systems, Security'},
  ]},
  { id:'s3', subject_name:'Thermodynamics', subject_code:'ME302', branch:'ME', semester:3, total_units:4, units:[
    {n:1,topic:'First law of thermodynamics'},
    {n:2,topic:'Second law & Entropy'},
    {n:3,topic:'Power & refrigeration cycles'},
    {n:4,topic:'Real gases, mixtures, psychrometry'},
  ]},
  { id:'s4', subject_name:'Database Management', subject_code:'IT402', branch:'IT', semester:4, total_units:5, units:[
    {n:1,topic:'ER Modeling, Relational model'},
    {n:2,topic:'SQL & Relational Algebra'},
    {n:3,topic:'Normalization (1NF–BCNF)'},
    {n:4,topic:'Transactions & Concurrency'},
    {n:5,topic:'Indexing & Query Processing'},
  ]},
];

let currentUser = {
  name: 'Aditya Kumar', role:'student', branch:'CSE', semester:4,
  college:'Indian Institute of Engineering',
  bio:'CS undergrad. Loves DSA, side projects, and sharing notes that actually help.',
  avatar:'https://api.dicebear.com/7.x/avataaars/svg?seed=Aditya&backgroundColor=6c63ff',
};

/* ===== SHARED UTILITIES ===== */

function showToast(msg) {
  const wrap = document.getElementById('toast-wrap');
  if (!wrap) return;
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = '✨ ' + msg;
  wrap.appendChild(t);
  setTimeout(() => t.remove(), 3200);
}

function initScrollProgress() {
  const bar = document.getElementById('scroll-progress');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const h = document.documentElement;
    const pct = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100 || 0;
    bar.style.width = pct + '%';
  }, { passive:true });
}

function initParticles() {
  const container = document.getElementById('particles');
  if (!container) return;
  const colors = ['#6c63ff','#00d4ff','#ff6b9d'];
  for (let i = 0; i < 36; i++) {
    const s = document.createElement('span');
    const size = Math.random()*3+1;
    const color = colors[i%3];
    s.style.cssText = `
      width:${size}px;height:${size}px;
      left:${Math.random()*100}%;top:${Math.random()*100}%;
      background:${color};opacity:.55;
      box-shadow:0 0 ${size*4}px ${color};
      --dur:${Math.random()*14+10}s;--delay:${Math.random()*-20}s;
    `;
    container.appendChild(s);
  }
}

function initRipple() {
  document.addEventListener('click', e => {
    const target = e.target.closest('.btn');
    if (!target) return;
    const rect = target.getBoundingClientRect();
    const r = document.createElement('span');
    const size = Math.max(rect.width, rect.height);
    r.className = 'ripple';
    r.style.width = r.style.height = size+'px';
    r.style.left = (e.clientX - rect.left - size/2)+'px';
    r.style.top  = (e.clientY - rect.top  - size/2)+'px';
    target.appendChild(r);
    setTimeout(() => r.remove(), 620);
  });
}

function initReveal() {
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('in'); });
  }, { threshold:0.1 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
}

function setActiveNav() {
  const page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link, .mobile-nav a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === page || (page === 'index.html' && href === 'index.html')) {
      a.classList.add('active');
    }
  });
}

function branchOptions(selected='all', allOption=true) {
  let html = allOption ? `<option value="all">All branches</option>` : '';
  BRANCHES.forEach(b => {
    html += `<option value="${b.code}" ${selected===b.code?'selected':''}>${b.code}</option>`;
  });
  return html;
}

function semOptions(selected='all', allOption=true) {
  let html = allOption ? `<option value="all">All semesters</option>` : '';
  for (let s=1; s<=8; s++) {
    html += `<option value="${s}" ${String(selected)===String(s)?'selected':''}>Sem ${s}</option>`;
  }
  return html;
}

function starsHTML(rating) {
  let html = '<div class="stars">';
  for (let i=1; i<=5; i++) html += `<span class="star ${i<=rating?'filled':''}">★</span>`;
  return html + '</div>';
}

function examLabel(t) {
  return t==='mid'?'Mid-Sem': t==='end'?'End-Sem':'Backlog';
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/[&<>]/g, function(m) {
    if (m === '&') return '&amp;';
    if (m === '<') return '&lt;';
    if (m === '>') return '&gt;';
    return m;
  });
}

function initCommon() {
    initScrollProgress();
    initParticles();
    initRipple();
    setTimeout(initReveal, 100);
    setActiveNav();

}