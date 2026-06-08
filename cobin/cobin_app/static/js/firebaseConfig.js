const firebaseConfig = window.COBIN_FIREBASE_CONFIG || {};

if (firebaseConfig.apiKey) {
    firebase.initializeApp(firebaseConfig);
    window.db = firebase.firestore();
    window.storage = firebase.storage();
} else {
    console.warn("Firebase config is not configured.");
}
