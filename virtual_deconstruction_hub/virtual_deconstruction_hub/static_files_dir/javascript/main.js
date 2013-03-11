function onSignUpClick(){
error = document.getElementById('error');
error.style.display = "none";
document.getElementById('username').style.border = "";
document.getElementById('password').style.border = "";
document.getElementById('confirmpassword').style.border = "";
document.getElementById('email').style.border = "";
document.getElementById('sameusername').style.display = "none";
var checkemail  = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;

if(document.getElementById('username').value == "" ){
	error.innerHTML = "You must select a valid username";
	error.style.display = "inline";
	document.getElementById('username').style.border = "1px solid #CD0A0A";
	return false;
}

if(document.getElementById('password').value == "" ){
	error.innerHTML = "You must select a valid password";
	error.style.display = "inline";
	document.getElementById('password').style.border = "1px solid #CD0A0A";
	return false;
}

if(document.getElementById('confirmpassword').value == "" ){
	error.innerHTML = "You must re-enter your password";
	error.style.display = "inline";
	document.getElementById('confirmpassword').style.border = "1px solid #CD0A0A";
	return false;
}




if(document.getElementById('email').value == "" ||  checkemail.test(document.getElementById('email').value) == false){
	error.innerHTML = "You must select a valid email address";
	error.style.display = "inline";
	document.getElementById('email').style.border = "1px solid #CD0A0A";
	return false;
}


if(document.getElementById('address').value == "" ){
	error.innerHTML = "You must enter an address";
	error.style.display = "inline";
	document.getElementById('address').style.border = "1px solid #CD0A0A";
	return false;
}

if(document.getElementById('city').value == "" ){
	error.innerHTML = "You must enter a city";
	error.style.display = "inline";
	document.getElementById('city').style.border = "1px solid #CD0A0A";
	return false;
}

if(document.getElementById('province').value == "" ){
	error.innerHTML = "You must select a province";
	error.style.display = "inline";
	document.getElementById('province').style.border = "1px solid #CD0A0A";
	return false;
}





if(document.getElementById('password').value != document.getElementById('confirmpassword').value){
	error.innerHTML = "Your passwords do not match";
	error.style.display = "inline";
	document.getElementById('password').style.border = "1px solid #CD0A0A";
	document.getElementById('confirmpassword').style.border = "1px solid #CD0A0A";
	return false;
}


}

 function onEditClick(){
 document.getElementById('email').style.border = "";
 var checkemail  = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
 
 if(document.getElementById('email').value == "" ||  checkemail.test(document.getElementById('email').value) == false){
	error.innerHTML = "You must select a valid email address";
	error.style.display = "inline";
	document.getElementById('email').style.border = "1px solid #CD0A0A";
	return false;
}
 
 }
 
 function cancelButton(){
 window.location.href="myaccount.html";
 }