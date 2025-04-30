document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById('coinChart').getContext('2d');
  const priceDisplay = document.getElementById("price");
  const coinSelect = document.getElementById("coinSelect");
  const chatSendBtn = document.getElementById("chat-send");
  const chatInput = document.getElementById("chat-message");
  const chatBox = document.getElementById("chat-box");

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
      responsive: true,
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

  async function fetchCandles(code) {
    const url = `https://api.upbit.com/v1/candles/minutes/1?market=${code}&count=30`;
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
    chart.data.datasets[0].label = code;
    chart.update();

    const latest = chartData[chartData.length - 1];
    priceDisplay.textContent = latest.c.toLocaleString();
  }

  let refreshInterval = null;

  function startAutoRefresh(code) {
    if (refreshInterval) clearInterval(refreshInterval);
    fetchCandles(code);
    refreshInterval = setInterval(() => fetchCandles(code), 30000); // 30초 간격
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
    startAutoRefresh(selectedCode);
    connectChat(selectedCode);
  });

  // 초기 실행
  const initialCode = coinSelect.value;
  startAutoRefresh(initialCode);
  connectChat(initialCode);
});
