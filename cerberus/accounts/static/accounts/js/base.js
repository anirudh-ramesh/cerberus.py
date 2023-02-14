function logout(){
    
    var access_token = localStorage.getItem("access_token")
    post_data = {CSRF: getCSRFTokenValue(), "access_token":access_token}
    $.post("/logout/", post_data, function(result){
        alert("Logout successfully");
        
    });
}

function delete_battery(){
    var battery_pack_sr_no = $("#delete_battery").data("model")
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(csrftoken)
    $.ajax({
        type: "POST",
        url: '/deletebattery/',
        headers:{'X-CSRFToken': csrftoken},
        data: {
            
            "battery_pack_sr_no":battery_pack_sr_no,
        },
        dataType: "json",
        success: function (data) {  
            alert("successfully Deleted")
        },
        
    });
    
}

$(document).ready(function(){

    $(document).on("click", "#logout_btn", logout);
    $(document).on("click", "#delete_battery", delete_battery);
    
});