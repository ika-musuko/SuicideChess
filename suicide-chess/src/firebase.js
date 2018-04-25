import firebase from 'firebase'
var config = {
    apiKey: "AIzaSyCcyyNLlr0XKkfwFP_EAsYX2i-ZLoIiPlQ",
    authDomain: "suicide-chess-dev.firebaseapp.com",
    databaseURL: "https://suicide-chess-dev.firebaseio.com",
    projectId: "suicide-chess-dev",
    storageBucket: "suicide-chess-dev.appspot.com",
    messagingSenderId: "721124950701"
  };
firebase.initializeApp(config);
export default firebase;
