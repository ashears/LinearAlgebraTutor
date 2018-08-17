function setCookie (name, value, day) {
	/* 
	Add/update cookie data
	For update data, use same cookie id. 
	input:
	   name: cookie id
	   value: cookie value (id, password)
	   day: expired date
	output:
		None
	*/
	var day = new Date();

	day.setTime(day.getTime() + (1000 * 24 * 60 * 60 * day));

	var expires = "expires=" + day.toUTCString();
	document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

function getCookie(name) {
	/*
	Get datat from cookie		
	input:
		name: cookie id
	output:
		returning string type cookie data 
	*/
	var cname = name + "=";
	var decoded_Cookie = decodeURIComponent(document.cookie);
	var cookieArr = decoded_Cookie.split(';');

	for (var i = 0; i < cookieArr.length; i++) {
		var c = cookieArr[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if(c.indexOf(name) == 0) {
			return c.substring(cname.length, c.length);
		}
	}

	return "";
}

function delCookie(name) {
	/* 
	delete cookie data by cookie data id 
	input:
		name: Cookie id
	output:
	   	None 
	*/
	document.cookie = name + "=; expires = Thu; 01 Jan 1970";
}

function delAllCookie() {
	/*
	deleting all the cookie data
	input:
		None
	output:
		None
	*/
	var cookies = document.cookie.split(";");

	for (var i = 0; i < cookies.length; i++) {
		var cookie = cookies[i];
		var eqPos = cookie.indexOf("=");
		var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
		delCookie(name);
	}
}