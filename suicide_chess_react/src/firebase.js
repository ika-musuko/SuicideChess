import firebase from 'firebase'
var config = {
    apiKey: "AIzaSyCXou2TZBE14UqO0ZuhOyCk8k-pBgSHkqQ",
    authDomain: "suicide-chess.firebaseapp.com",
    databaseURL: "https://suicide-chess-dev1.firebaseio.com",
    projectId: "suicide-chess",
    storageBucket: "suicide-chess.appspot.com",
    messagingSenderId: "306643895755"
  };
firebase.initializeApp(config);
export default firebase;
