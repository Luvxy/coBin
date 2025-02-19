function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  document.getElementById('imageUpload').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (!file) {
        console.log('파일이 선택되지 않았습니다.');
        return;
    }
    
    console.log('선택된 파일:', file.name);

    const formData = new FormData();
    formData.append('image', file);

    fetch('/upload_user_image/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('서버 응답:', data);
        if (data.status === 'success') {
            document.getElementById('profileImage').src = data.image_url;
        } else {
            console.error('업로드 실패:', data.reason);
            alert('이미지 업로드 실패: ' + data.reason);
        }
    })
    .catch(error => {
        console.error('Fetch 오류:', error);
        alert('서버와 통신 중 오류가 발생했습니다.');
    });
});
