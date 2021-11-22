let gamburger = document.getElementById("gamburger");
let profileBtns = document.getElementById("profile-btn");
let regBtn = profileBtns.querySelector(".logIn");
let loginBtn = profileBtns.querySelector(".register");

gamburger.addEventListener("click", ()=>{
    profileBtns.classList.toggle("active-profile-mobile");
    regBtn.classList.toggle("active-mobile-login");
    loginBtn.classList.toggle("active-mobile-reg");

});