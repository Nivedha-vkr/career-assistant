const form =document.querySelector('#form')
const username =document.querySelector('#username')
const email =document.querySelector('#email')
const password=document.querySelector('#password')
const cpassword =document.querySelector('#cpassword')

form.addEventListener('submit',(e)=>{
    if(!validateInput()){
        e.preventDefault();
    }

});
function validateInput(){
    const usernameVal=username.value.trim();
    const emailVal=email.value.trim();
    const passwordVal=password.value.trim();
    const cpasswordVal=cpassword.value.trim();
    let success=true;
    //username validation
    if(usernameVal===""){
        success=false;
        setError(username, 'username is required');
    }
    else{
        setSuccess(username);
}

if(emailVal===""){
    success=false;
    setError(email,'Email is required')
}
else if(!validateEmail(emailVal))
{
    setError(email, 'please enter a valid email')
}
else{
    setSuccess(email)
}
if(passwordVal===''){
    success=false;
    setError(password, 'password is required')
}
else if(passwordVal.length<8){
    setError(password, 'password must be 8 characters long')
}
else{
    setSuccess(password)
}
if (cpasswordVal === "") {
        success = false;
        setError(cpassword, "Please confirm your password");
    } else if (cpasswordVal !== passwordVal) {
        success = false;
        setError(cpassword, "Passwords do not match");
    } else {
        setSuccess(cpassword);
    }

    return success;
}

function setError(element, message){
    const inputGroup=element.parentElement;
    const errorElement=inputGroup.querySelector('.error');
    errorElement.innerText=message;
    inputGroup.classList.add('error');
    inputGroup.classList.remove('success');
}
function setSuccess(element){
    const inputGroup=element.parentElement;
    const errorElement=inputGroup.querySelector('.error');
    errorElement.innerText='';
    inputGroup.classList.add('success');
    inputGroup.classList.remove('error');
}
function validateEmail(email){
    return String(email)
        .toLowerCase()
        .match(
            // Regex for basic email validation
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/


        );
}


document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            const email = document.getElementById("loginEmail").value.trim();
            const password = document.getElementById("loginPassword").value.trim();

            if (!email || !password) {
                alert("Please fill out all fields!");
                event.preventDefault();
            }
        });
    }
});



/** 
// ===== SIDE MENU TOGGLE =====
const menuToggle = document.getElementById('menu-toggle');
const sideMenu = document.getElementById('side-menu');

menuToggle.addEventListener('click', () => {
  sideMenu.classList.toggle('active');
});


const form = document.querySelector('#form');
const username = document.querySelector('#username');
const email = document.querySelector('#email');
const password = document.querySelector('#password');
const cpassword = document.querySelector('#cpassword');

// Check if we're on signup page or login page
if (form && username && cpassword) {
    // --------- SIGNUP FORM VALIDATION ---------
    form.addEventListener('submit', (e) => {
        if (!validateSignup()) {
            e.preventDefault();
        }
    });

    function validateSignup() {
        const usernameVal = username.value.trim();
        const emailVal = email.value.trim();
        const passwordVal = password.value.trim();
        const cpasswordVal = cpassword.value.trim();
        let success = true;

        // Username validation
        if (usernameVal === "") {
            success = false;
            setError(username, 'Username is required');
        } else {
            setSuccess(username);
        }

        // Email validation
        if (emailVal === "") {
            success = false;
            setError(email, 'Email is required');
        } else if (!validateEmail(emailVal)) {
            success = false;
            setError(email, 'Please enter a valid email');
        } else {
            setSuccess(email);
        }

        // Password validation
        if (passwordVal === '') {
            success = false;
            setError(password, 'Password is required');
        } else if (passwordVal.length < 8) {
            success = false;
            setError(password, 'Password must be at least 8 characters');
        } else {
            setSuccess(password);
        }

        // Confirm password validation
        if (cpasswordVal === "") {
            success = false;
            setError(cpassword, "Please confirm your password");
        } else if (cpasswordVal !== passwordVal) {
            success = false;
            setError(cpassword, "Passwords do not match");
        } else {
            setSuccess(cpassword);
        }

        return success;
    }
} else if (form && email && password) {
    // --------- LOGIN FORM VALIDATION ---------
    form.addEventListener('submit', (e) => {
        if (!validateLogin()) {
            e.preventDefault();
        }
    });

    function validateLogin() {
        const emailVal = email.value.trim();
        const passwordVal = password.value.trim();
        let success = true;

        if (emailVal === "") {
            success = false;
            setError(email, "Email is required");
        } else if (!validateEmail(emailVal)) {
            success = false;
            setError(email, "Please enter a valid email");
        } else {
            setSuccess(email);
        }

        if (passwordVal === "") {
            success = false;
            setError(password, "Password is required");
        } else {
            setSuccess(password);
        }

        return success;
    }
}

// Helper functions
function setError(element, message) {
    const inputGroup = element.parentElement;
    let errorElement = inputGroup.querySelector('.error');
    if (!errorElement) {
        errorElement = document.createElement('small');
        errorElement.classList.add('error');
        inputGroup.appendChild(errorElement);
    }
    errorElement.innerText = message;
    inputGroup.classList.add('error');
    inputGroup.classList.remove('success');
}

function setSuccess(element) {
    const inputGroup = element.parentElement;
    const errorElement = inputGroup.querySelector('.error');
    if (errorElement) {
        errorElement.innerText = '';
    }
    inputGroup.classList.add('success');
    inputGroup.classList.remove('error');
}

function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.toLowerCase());
}


// Wait for DOM to load
document.addEventListener("DOMContentLoaded", function () {
    // Handle signup form validation
    const signupForm = document.querySelector("#signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", function (e) {
            const username = document.querySelector("#signupUsername").value.trim();
            const email = document.querySelector("#signupEmail").value.trim();
            const password = document.querySelector("#signupPassword").value.trim();
            const cpassword = document.querySelector("#signupCpassword").value.trim();

            // Username check
            if (username.length < 3) {
                alert("Username must be at least 3 characters long!");
                e.preventDefault();
                return;
            }

            // Email check (basic regex)
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(email)) {
                alert("Please enter a valid email address!");
                e.preventDefault();
                return;
            }

            // Password strength check
            if (password.length < 6) {
                alert("Password must be at least 6 characters long!");
                e.preventDefault();
                return;
            }

            // Confirm password match
            if (password !== cpassword) {
                alert("Passwords do not match!");
                e.preventDefault();
                return;
            }
        });
    }

    // Handle login form validation
    const loginForm = document.querySelector("#loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            const email = document.querySelector("#loginEmail").value.trim();
            const password = document.querySelector("#loginPassword").value.trim();

            // Email check
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(email)) {
                alert("Please enter a valid email address!");
                e.preventDefault();
                return;
            }

            // Password check
            if (password.length < 6) {
                alert("Password must be at least 6 characters long!");
                e.preventDefault();
                return;
            }
        });
    }
});
**/
