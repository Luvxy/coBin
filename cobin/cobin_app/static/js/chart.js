document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById('coinChart').getContext('2d');
  const priceDisplay = document.getElementById("price");
  const coinSelect = document.getElementById("coinSelect");
  const chatSendBtn = document.getElementById("chat-send");
  const chatInput = document.getElementById("chat-message");
  const chatBox = document.getElementById("chat-box");
  const timeUnitSelector = document.getElementById("time-unit-selector");

  let chart = new Chart(ctx, {
    type: 'candlestick',
    data: {
      datasets: [{
        label: '',
        data: [],
        borderColor: '#999',
        borderWidth: 1,
        barThickness: 8,
        color: {
          up: '#ff2e63',
          down: '#08d9d6',
          unchanged: '#999'
        }
      }]
    },
    options: {
      responsive: true, // 반응형 활성화
      maintainAspectRatio: true, // 캔버스 비율 유지 비활성화
      animation: false,
      parsing: false,
      scales: {
        x: {
          type: 'time',
          grid: { display: false },
          time: { unit: 'minute', tooltipFormat: 'HH:mm' },
          ticks: { color: '#333' }
        },
        y: {
          grid: { display: false },
          ticks: { color: '#333' }
        }
      },
      plugins: {
        legend: {
          labels: { color: '#333' }
        }
      }
    }
  });

  async function fetchCandles(code, timeUnit) {
    const timeUnitMap = {
      minute1: 1,
      minute3: 3,
      minute5: 5,
      minute10: 10,
      minute15: 15,
      minute30: 30,
      minute60: 60,
      minute240: 240,
      day: 'days'
    };

    const unit = timeUnitMap[timeUnit] || 1; // 기본값 1분
    const url = `https://api.upbit.com/v1/candles/minutes/${unit}?market=${code}&count=50`;
    const response = await fetch(url);
    const rawData = await response.json();

    const chartData = rawData.reverse().map(item => ({
      x: new Date(item.candle_date_time_kst),
      o: item.opening_price,
      h: item.high_price,
      l: item.low_price,
      c: item.trade_price
    }));

    chart.data.datasets[0].data = chartData;
    chart.data.datasets[0].label = `${code} (${timeUnit})`;
    chart.update();

    const latest = chartData[chartData.length - 1];
    priceDisplay.textContent = latest.c.toLocaleString();
  }

  let refreshInterval = null;

  function startAutoRefresh(code, timeUnit) {
    if (refreshInterval) clearInterval(refreshInterval);
    fetchCandles(code, timeUnit);
    refreshInterval = setInterval(() => fetchCandles(code, timeUnit), 1000); // 30초 간격
  }

  // 채팅
  let chatSocket;
  let lastSentTime = 0;

  function connectChat(code) {
    if (chatSocket) chatSocket.close();

    chatBox.innerHTML = ""; // 이전 채팅 지우기

    chatSocket = new WebSocket('ws://' + window.location.host + `/ws/chat/${code}/`);

    chatSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      const msg = document.createElement("div");

      if (data.timestamp) {
        msg.innerHTML = `<span style="color:#999">[${data.timestamp}]</span> <b>${data.username}</b>: ${data.message}`;
      } else {
        msg.textContent = `${data.username}: ${data.message}`;
      }

      chatBox.appendChild(msg);
      chatBox.scrollTop = chatBox.scrollHeight;
    };
  }

  chatSendBtn.onclick = () => {
    const now = Date.now();
    const message = chatInput.value.trim();

    if (!message) return;
    if (message.length > 60) {
      alert("메시지는 최대 60자까지 가능합니다.");
      return;
    }

    if (now - lastSentTime < 1000) {
      alert("1초에 한 번만 전송할 수 있습니다.");
      return;
    }

    chatSocket.send(JSON.stringify({ message }));
    chatInput.value = "";
    lastSentTime = now;
  };

  chatInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      chatSendBtn.click();
    }
  });

  coinSelect.addEventListener("change", function () {
    const selectedCode = this.value;
    const selectedTimeUnit = timeUnitSelector.value;
    startAutoRefresh(selectedCode, selectedTimeUnit);
    connectChat(selectedCode);
  });

  timeUnitSelector.addEventListener("change", function () {
    const selectedCode = coinSelect.value;
    const selectedTimeUnit = this.value;
    startAutoRefresh(selectedCode, selectedTimeUnit);

    // WebSocket 메시지 전송
    chartSocket.send(JSON.stringify({
      code: selectedCode,
      time_unit: selectedTimeUnit
    }));
    console.log(`시간 단위 변경: ${selectedTimeUnit}`);
  });

  // 초기 실행
  const initialCode = coinSelect.value;
  const initialTimeUnit = timeUnitSelector.value;
  startAutoRefresh(initialCode, initialTimeUnit);
  connectChat(initialCode);

  // WebSocket for chart updates
  const chartSocket = new WebSocket("ws://127.0.0.1:8000/ws/chart/");

  chartSocket.onopen = function () {
    console.log("WebSocket 연결 성공");

    // 초기 값 전송
    chartSocket.send(JSON.stringify({
      code: initialCode,
      time_unit: initialTimeUnit
    }));
  };

  chartSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log("서버로부터 받은 데이터:", data);

    // 차트 업데이트 로직 추가
    const chart = document.getElementById("chart");
    chart.innerText = `현재 가격: ${data.price}`;
  };

  const chartContainer = document.querySelector(".chart-container");
  const coinChart = document.getElementById("coinChart");

  let isDragging = false;
  let startX = 0;
  let scrollLeft = 0;

  // 마우스 다운 이벤트
  chartContainer.addEventListener("mousedown", (e) => {
    isDragging = true;
    chartContainer.classList.add("dragging");
    startX = e.pageX - chartContainer.offsetLeft;
    scrollLeft = chartContainer.scrollLeft;
  });

  // 마우스 이동 이벤트
  chartContainer.addEventListener("mousemove", (e) => {
    if (!isDragging) return; // 드래그 중이 아닐 경우 무시
    e.preventDefault();
    const x = e.pageX - chartContainer.offsetLeft;
    const walk = (x - startX) * 2; // 드래그 속도 조정
    chartContainer.scrollLeft = scrollLeft - walk;
  });

  // 마우스 업 및 마우스 아웃 이벤트
  chartContainer.addEventListener("mouseup", () => {
    isDragging = false;
    chartContainer.classList.remove("dragging");
  });

  chartContainer.addEventListener("mouseleave", () => {
    isDragging = false;
    chartContainer.classList.remove("dragging");
  });
});
