function logout(){
    
    var access_token = localStorage.getItem("access_token")
    post_data = {"access_token":access_token}
    $.post("/logout/", post_data, function(result){
        alert("Logout successfully");
        
    });
}

function battery_tab(){
    
}

$(document).ready(function(){

    $(document).on("click", "#logout_btn", logout);
    
});