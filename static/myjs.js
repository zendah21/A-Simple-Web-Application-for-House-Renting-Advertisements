
// This function is called to validate the form for any empty fields
function validate_empty(formName, field)
{
	// Get the form
	var form = document.forms[formName];

	// Get the value of the field
	var field_value = form[field].value;
	// Get the error element
	var error = document.getElementById(field+"_error");

	// If the field is empty, display the error message
	if(field_value == "")
	{
		error.innerHTML = field.charAt(0).toUpperCase()+field.slice(1)+" is mandatory!";
		error.style.display = "block";
	}
	else
	{
		error.innerHTML = "";
		error.style.display = "none";
	}

	// Return true if the field is not empty
	return field_value != "";
}

// This function is called to validate the form for username field
function validate_username(formName){

	var error = document.getElementById("username_error");

	validate_empty(formName, "username");

	return error.innerHTML;
}

// This function is called to validate the form for password field
function validate_password(formName){

	var form = document.forms[formName];
	var password = form["password"].value;
	var error = document.getElementById("password_error");

	if(validate_empty(formName, "password"))
	{
		// Check if the password contains an upper case letter otherwise show error
		if(countSequence("ABCDEFGHIJKLMNOPQRSTUVWXYZ", password) == 0)
		{
			error.innerHTML = "Password should include at least one capital letter!";
			error.style.display = "block";
			return error.innerHTML;
		}
		// Check if the password contains a lower case letter otherwise show error
		if(countSequence("abcdefghijklmnopqrstuvwxyz", password) == 0)
		{
			error.innerHTML = "Password should include at least one small letter!";
			error.style.display = "block";
			return error.innerHTML;
		}
		// Check if the password contains a digit otherwise show error
		if(countSequence("0123456789", password) == 0)
		{
			error.innerHTML = "Password should include at least one digit!";
			error.style.display = "block";
			return error.innerHTML;
		}
		// Check if the password contains a special character otherwise show error
		if(countSequence("+!*-", password) == 0)
		{
			error.innerHTML = "Password should include at least one special character!";
			error.style.display = "block";
			return error.innerHTML;
		}
		// Check if the password is at least 10 characters long otherwise show error
		if(password.length<10)
		{
			error.innerHTML = "Password should be at least 10 characters long!";
			error.style.display = "block";
			return error.innerHTML;
		}

		error.innerHTML = "";
		error.style.display = "none";
		return "";
	}
	return error.innerHTML;
}

// This function is called to validate the form for fullname field
function validate_fullname(formName){

	var error = document.getElementById("fullname_error");

	validate_empty(formName,"fullname");
	return error.innerHTML;
}

// This function is called to validate the form for email field
function validate_email(formName){

	var error = document.getElementById("email_error");

	validate_empty(formName,"email");
	return error.innerHTML;
}

// This function is called to validate the form for telephone field
function validate_telephone(formName){

	var error = document.getElementById("telephone_error");

	validate_empty(formName,"telephone")
	return error.innerHTML;
}

// This function is called to validate the form for all fields
function validate_form(formName){

	document.getElementById("form_errors").style.display = "none";
	document.getElementById("form_errors").innerHTML = "";

	var form = document.forms[formName];

	var username = form["username"].value;
	var password = form["password"].value;
	var fullname = form["fullname"].value;
	var email = form["email"].value;
	var telephone = form["telephone"].value;

	var all_valid = [];

	all_valid.push(validate_username(formName));
	all_valid.push(validate_password(formName));
	all_valid.push(validate_fullname(formName));
	all_valid.push(validate_email(formName));
	all_valid.push(validate_telephone(formName));

	var all_errors = all_valid.join("");

	// If there are any errors, display them
	if(all_errors != "")
	{
		//var xmlhttp = new XMLHttpRequest();
		//xmlhttp.open("POST", "/display_register_errors", true);
		//xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		all_errors = all_valid.join("<br/>");
		document.getElementById("form_errors").innerHTML = all_errors;
		document.getElementById("form_errors").style.display = "block";
		//xmlhttp.send("errors="+all_errors);
		return false;
	}

	return true;
}

// Counts the number of characters in a string that are present in another string
function countSequence(sequence, str){
	var i = 0;
	var counter = 0;

	for(; i<str.length; i++)
		if(sequence.search(str[i]) != -1)
			counter++;

	return counter;
}

// This function is called to submit the form
function submitForm(formName){
	var form = document.forms[formName];
	form.submit();
}