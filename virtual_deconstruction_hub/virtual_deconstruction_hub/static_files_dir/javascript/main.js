function showErrorAndFocus(errorfield, errormsg, element)
{
    errorfield.innerHTML = errormsg;
    errorfield.style.display = "inline";
    element.style.border = "2px solid #CD0A0A"; 
    element.focus();
}

function onSignUpClick(){
error = document.getElementById('error');
error.style.display = "none";
document.getElementById('password').style.border = "";
document.getElementById('confirmpassword').style.border = "";
document.getElementById('email').style.border = "";
document.getElementById('address').style.border = "";
document.getElementById('city').style.border = "";
document.getElementById('province').style.border = "";

if (document.getElementById('sameusername'))
    document.getElementById('sameusername').style.display = "none";

var checkemail  = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;

if(document.getElementById('email').value == "" ||  checkemail.test(document.getElementById('email').value) == false){
    showErrorAndFocus(error, "You must select a valid email address", document.getElementById('email'));
	return false;
}

if(document.getElementById('password').value == "" ){
    showErrorAndFocus(error, "You must select a valid password", document.getElementById('password'));
	return false;
}

if(document.getElementById('confirmpassword').value == "" ){
    showErrorAndFocus(error, "You must re-enter your password", document.getElementById('confirmpassword'));
	return false;
}

if(document.getElementById('password').value != document.getElementById('confirmpassword').value){
	error.innerHTML = "Your passwords do not match";
	error.style.display = "inline";
	document.getElementById('password').style.border = "2px solid #CD0A0A";
	document.getElementById('confirmpassword').style.border = "2px solid #CD0A0A";
    document.getElementById('confirmpassword').focus();
	return false;
}

if(document.getElementById('address').value == "" ){
    showErrorAndFocus(error, "You must enter an address", document.getElementById('address'));
	return false;
}

if(document.getElementById('city').value == "" ){
    showErrorAndFocus(error, "You must select a city", document.getElementById('city'));
	return false;
}

if(document.getElementById('province').value == "" ){
    showErrorAndFocus(error, "You must select a province", document.getElementById('province'));
	return false;
}

return true;
}

function onEditClick(){
    error = document.getElementById('error');
    error.style.display = "none";
    document.getElementById('password').style.border = "";
    document.getElementById('confirmpassword').style.border = "";
    document.getElementById('address').style.border = "";
    document.getElementById('city').style.border = "";
    document.getElementById('province').style.border = "";
    var checkemail  = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
 
    if(document.getElementById('password').value != "" && document.getElementById('password').value != document.getElementById('confirmpassword').value){
        error.innerHTML = "Your passwords do not match";
        error.style.display = "inline";
        document.getElementById('password').style.border = "2px solid #CD0A0A";
        document.getElementById('confirmpassword').style.border = "2px solid #CD0A0A";
        document.getElementById('confirmpassword').focus();
        return false;
    }

    if(document.getElementById('address').value == "" ){
        showErrorAndFocus(error, "You must enter an address", document.getElementById('address'));
        return false;
    }

    if(document.getElementById('city').value == "" ){
        showErrorAndFocus(error, "You must select a city", document.getElementById('city'));
        return false;
    }

    if(document.getElementById('province').value == "" ){
        showErrorAndFocus(error, "You must select a province", document.getElementById('province'));
        return false;
    }
}
 
function cancelButton(){
    window.location.href="profile";
}
 
function checkLogin(){
    document.getElementById('username').style.border = "";
    document.getElementById('password').style.border = "";
    error = document.getElementById('error');
    if (document.getElementById('sameusername'))
        document.getElementById('sameusername').style.display = "none";
 
    if(document.getElementById('username').value == "" ){
        showErrorAndFocus(error, "Please enter your username", document.getElementById('username'));
        return false;
    }

    if(document.getElementById('password').value == "" ){
        showErrorAndFocus(error, "You must enter a password", document.getElementById('password'));
        return false;
    }
 
}
 
function checkNewPost(){
    document.getElementById('id_title').style.border = "";
    document.getElementById('id_price').style.border = "";
    document.getElementById('detail_address').style.border = "";
    document.getElementById('detail_text_content').style.border = "";
    error = document.getElementById('error');
    
    if(document.getElementById('id_title').value == "" ){
        showErrorAndFocus(error, "Please enter a title", document.getElementById('id_title'));
        return false;
    }

    if(document.getElementById('detail_text_content').value == "" ){
        showErrorAndFocus(error, "Please enter enter a description", document.getElementById('detail_text_content'));
        return false;
    }
} 
 
function checkNewBlog()
{
    document.getElementById('id_title').style.border = "";
    document.getElementById('id_text_content').style.border = "";
    error = document.getElementById('error');
    
    if(document.getElementById('id_title').value == "" ){
        showErrorAndFocus(error, "Please enter a title", document.getElementById('id_title'));
        return false;
    }
    if(document.getElementById('id_text_content').value == "" ){
        showErrorAndFocus(error, "Please enter enter some content", document.getElementById('id_text_content'));
        return false;
    }
}

function checkContactFields()
{
    document.getElementById('emailTxt').style.border = "";
    document.getElementById('emailSubject').style.border = "";
    document.getElementById('emailMsg').style.border = "";
    error = document.getElementById('error');
    
    if(document.getElementById('emailTxt').value == "" ){
        showErrorAndFocus(error, "Please enter your email address", document.getElementById('emailTxt'));
        return false;
    }
    
    if(document.getElementById('emailSubject').value == "" ){
        showErrorAndFocus(error, "Please enter a subject", document.getElementById('emailSubject'));
        return false;
    }
    
    if(document.getElementById('emailMsg').value == "" ){
        showErrorAndFocus(error, "Please enter your message", document.getElementById('emailMsg'));
        return false;
    }
}

function setDDL(ddl, value)
{
    for (var i=0; i< ddl.length; i++){
        if (ddl.options[i].value == value)
            ddl.options[i].selected = "selected"
    }
}  
 
 function isNumberKey(evt)
      {
         var charCode = (evt.which) ? evt.which : event.keyCode
         if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;

         return true;
      }
      
 function addAnotherPicture()
 {
 
 document.getElementById('pictureform').value = "1";
 if (document.getElementById('id_picture').value == ""){
 alert("You must choose a file to add");
 return false;
 }
 }
 
  function setSubmitTrue()
 {
 
 document.getElementById('issubmit').value = "1";
 }
 
 function listedmost(){
 	removeHoverBackground();
 	hideAllPictures();
 	document.getElementById("listedmost").style.background = "#00dd68"
 	document.getElementById('surveycategoryrank').style.display = 'inline';
 	reAddHover();
 
 }
 function highestsale(){
 	removeHoverBackground();
 	hideAllPictures();
 	document.getElementById("highestsale").style.background = "#00dd68"
 	document.getElementById('sellercategoryrank').style.display = 'inline';
 	reAddHover();
 }
 function boughtmost(){
  	removeHoverBackground();
 	hideAllPictures();
 	document.getElementById("boughtmost").style.background = "#00dd68"
 	document.getElementById('buyercategoryrank').style.display = 'inline';
 	reAddHover();
 	
 }
 function averagetransactioneach(){
  	removeHoverBackground();
 	hideAllPictures();
 	document.getElementById("averagetransactioneach").style.background = "#00dd68"
 	document.getElementById('categorytransactionamount').style.display = 'inline';
 	reAddHover();
 	
 }
 function averagetransactionamount(){
  	removeHoverBackground();
 	hideAllPictures();
 	document.getElementById("averagetransactionamount").style.background = "#00dd68"
 	document.getElementById('amountsellerbuyer').style.display = 'inline';
 	reAddHover();
 	
 }
 function transactiontime(){
  	removeHoverBackground();
 	hideAllPictures();
 	document.getElementById("transactiontime").style.background = "#00dd68"
 	document.getElementById('averagetransactiontime').style.display = 'inline';
 	reAddHover();
 	
 }
 function ratesucess(){
  	removeHoverBackground();
 	hideAllPictures();
 	document.getElementById("ratesucess").style.background = "#00dd68"
 	document.getElementById('successrate').style.display = 'inline';
 	reAddHover();
 	
 }
 
 function removeHoverBackground(){
	document.getElementById("listedmost").style.background = "black"
	document.getElementById("highestsale").style.background = "black"
	document.getElementById("boughtmost").style.background = "black"
	document.getElementById("averagetransactioneach").style.background = "black"
	document.getElementById("averagetransactionamount").style.background = "black"
	document.getElementById("transactiontime").style.background = "black"
	document.getElementById("ratesucess").style.background = "black"
       
 }
 
 
 function hideAllPictures()
 {
 	document.getElementById('surveycategoryrank').style.display = 'none';
 	document.getElementById('successrate').style.display = 'none';
  	document.getElementById('averagetransactiontime').style.display = 'none';
  	document.getElementById('amountsellerbuyer').style.display = 'none';
  	document.getElementById('categorytransactionamount').style.display = 'none';
  	document.getElementById('sellercategoryrank').style.display = 'none';
  	document.getElementById('buyercategoryrank').style.display = 'none';
 }

function reAddHover()
{
	document.styleSheets[0].insertRule('#itemsinlist:hover { background-color: #00dd68; }', 0);
}