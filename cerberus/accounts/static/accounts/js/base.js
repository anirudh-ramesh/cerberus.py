function logout(){
    
    var access_token = localStorage.getItem("access_token")
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    $.ajax({
        type: "POST",
        url: '/logout/',
        headers:{'X-CSRFToken': csrftoken},
        data: {
            "access_token":access_token,
        },
        dataType: "json",
        success: function (data) {  
            alert("successfully Logged out")
        },
        
    });
}

function delete_battery(){
    
    var battery_pack_sr_no = $("#delete_battery").data("model");
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(csrftoken, 'aksdhvkjasvdkjasd')
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


function password_hide(){
    $("#password").prop("type", "password");
    $("#hide_password").hide();
    $("#show_password").show();
}


function password_show(){
    $("#password").prop("type", "text");
    $("#hide_password").show();
    $("#show_password").hide();
}

function update_battery(){
    
    // var battery_pack_sr_no = $(this).data("battery_pack_sr_no")
    battery_pack_sr_no = $("#updated_battery_pack_sr_no").data("model");
    var model_name = $(this).data("model_name")
    console.log("sssssssssddddd battery pack",battery_pack_sr_no)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // $("#updated_model_name").val(model_name)
    // $("#updated_battery_pack_sr_no").val(battery_pack_sr_no)
    url='/update_battery/'+battery_pack_sr_no
    // $.ajax({
    //     type: "POST",
    //     url: url,
    //     headers:{'X-CSRFToken': csrftoken},
    //     data: {
            
    //         "battery_pack_sr_no":battery_pack_sr_no,
    //     },
    //     // dataType: "json",
    //     success: function (data) {  
    //         alert("successfully Deleted")
    //     },
        
    // });
}


$(document).ready(function(){
    $("#hide_password").hide();

    $(document).on("click", "#logout_btn", logout);
    $(document).on("click", "#delete_battery", delete_battery);
    $(document).on("click", "#update_battery", update_battery);
    $(document).on("click", "#show_password", password_show);
    $(document).on("click", "#hide_password", password_hide);
    
});
