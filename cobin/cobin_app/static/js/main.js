// app.js
/* ===== helper: fetch JSON util (API 연결 시 편의용) ===== */
async function fetchJSON(url){
    const res = await fetch(url);
    if(!res.ok){throw new Error('Network error');}
    return await res.json();
  }
  
  /* ===== recent-post 영역 업데이트 (더미 데이터 → API 연결) ===== */
  async function loadRecentPosts(){
    try{
      // const posts = await fetchJSON('/api/recent-posts');
      const posts = [
        {id:101,title:'RSI 전략 질문드립니다.'},
        {id:102,title:'새로운 지표 조합 공유!'},
        {id:103,title:'업데이트 v1.2 릴리즈 노트'},
        {id:104,title:'4월 수익 인증 ☑️'},
        {id:105,title:'자동 매매 실패 후기…'}
      ];
      const ul = document.getElementById('recent-list');
      ul.innerHTML = '';
      posts.forEach(p=>{
        const li = document.createElement('li');
        li.innerHTML = `<a href="/posts/${p.id}">${p.title}</a>`;
        ul.appendChild(li);
      });
    }catch(e){console.error(e);}
  }
  
  /* ===== 베스트 파일럿 랭킹 업데이트 ===== */
  async function loadPilotRanking(){
    try{
      // const ranking = await fetchJSON('/api/pilot-ranking');
      const ranking = [
        {nick:'홍길동',profit:153},
        {nick:'김무사',profit:131},
        {nick:'이영희',profit:122},
        {nick:'traderK',profit:116},
        {nick:'alpha',profit:104},
        {nick:'beta',profit:99},
        {nick:'gamma',profit:96},
        {nick:'delta',profit:90},
        {nick:'omega',profit:88},
        {nick:'sigma',profit:82}
      ];
  
      // 1~3위
      document.getElementById('pilot-1-nick').textContent = ranking[0].nick;
      document.getElementById('pilot-2-nick').textContent = ranking[1].nick;
      document.getElementById('pilot-3-nick').textContent = ranking[2].nick;
  
      // 4~10위
      const tbody = document.querySelector('#pilot-table tbody');
      tbody.innerHTML = '';
      ranking.slice(3).forEach((p,idx)=>{
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${idx+4}</td><td>${p.nick}</td><td>${p.profit}%</td>`;
        tbody.appendChild(tr);
      });
  
      // 검색
      document.getElementById('pilot-search-btn').onclick = ()=>{
        const q = document.getElementById('pilot-search').value.trim().toLowerCase();
        tbody.querySelectorAll('tr').forEach(tr=>{
          const nick = tr.children[1].textContent.toLowerCase();
          tr.style.display = nick.includes(q)?'':'none';
        });
      };
    }catch(e){console.error(e);}
  }
  
  /* ===== init ===== */
  document.addEventListener('DOMContentLoaded',()=>{
    loadRecentPosts();
    loadPilotRanking();
  
    // 10초마다 자동 갱신 – 필요에 따라 조정
    setInterval(loadRecentPosts,60_000);
    setInterval(loadPilotRanking,60_000);
  });
  