function validateForm(){
    document.getElementById("pFirstName").innerHTML = "";
    document.getElementById("pLastName").innerHTML = "";

    const firstName = document.forms[ "userForm"][ "firstName"].value;
    if (!validSingleWord(firstName)) {
        document.getElementById("pFirstName").innerHTML = "First Name not acceptable";
        return false;
    }
    
    const lastName = document.forms[ "userForm"][ "lastName"].value;
    if (!validSingleWord(lastName)) {
        document.getElementById("pLastName").innerHTML = "Last Name not acceptable";
        return false;
    }

    const dateOfBirth = document.forms[ "userForm"][ "dateOfBirth"].value;
    if ( ageFromYear(dateOfBirth) < 13 ) {
        document.getElementById("pDateOfBirth").innerHTML = "Too young";
        return false;
    }
    
    return true;
    }
   
function validSingleWord( s ) {
    if ( s.length === 0 ) return false; // 0 length
    if ( !isNaN( s - parseFloat( s ))) return false; // number
    if ( s.indexOf(" ") != -1 ) return false; // if there's a space
    return true;
}

function ageFromYear ( d ) {
    // yyyy-mm-dd
    let year = d.split( "-" )[0];
    let curr = new Date().getFullYear();
    return curr - year;
}