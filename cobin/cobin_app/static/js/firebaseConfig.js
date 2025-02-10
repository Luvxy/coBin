// Firebase 설정
const firebaseConfig = {
    apiKey: "AIzaSyCBw6nSO3pCmlIitUnspHJRtIXQO4pFl8I",
    authDomain: "cob2n-c0ece.firebaseapp.com",
    projectId: "cob2n-c0ece",
    storageBucket: "cob2n-c0ece.firebasestorage.app",
    messagingSenderId: "526705145192",
    appId: "1:526705145192:web:b0e529d947d224df5352dd",
    measurementId: "G-W23YJX7WZN"
};

// Firebase 초기화
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
const storage = firebase.storage();
