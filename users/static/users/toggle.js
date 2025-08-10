document.addEventListener('DOMContentLoaded', () => {
    const toggleButton1 = document.getElementById('toggleIcon1');
    const passwordInput1 = document.getElementById("password1");
    toggleButton1.addEventListener('click', () => {
        
        if (passwordInput1.type === "password") {
            passwordInput1.type = "text";
            toggleButton1.classList.remove("fa-eye-slash");
            toggleButton1.classList.add("fa-eye");
        } else {
            passwordInput1.type = "password";
            toggleButton1.classList.remove("fa-eye");
            toggleButton1.classList.add("fa-eye-slash");
        }
    });



    const toggleButton2 = document.getElementById('toggleIcon2');
    const passwordInput2 = document.getElementById('password2');

    toggleButton2.addEventListener('click',() =>{
        
        if(passwordInput2.type === "password"){
            passwordInput2.type = "text";
            toggleButton2.classList.remove("fa-eye-slash");
            toggleButton2.classList.add("fa-eye");
        }
        else{
            passwordInput2.type = "password";
            toggleButton2.classList.remove("fa-eye");
            toggleButton2.classList.add("fa-eye-slash");
        
        }

    });

});
