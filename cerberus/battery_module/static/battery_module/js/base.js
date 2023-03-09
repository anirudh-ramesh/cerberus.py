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

// function allocate_battery_fun(){
//     debugger;
//     // a=document.getElementById("allocate_battery_pack_sr_no1")
//     var battery_pack_sr_no = $("#updated_battery_pack_sr_no2").val();
//     // var model_name = $("#updated_model_name").data("model");
//     var model_name = $("#updated_model_name").val();
//     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//     console.log("sssss",battery_pack_sr_no,model_name)
//     $.ajax({
//         type: "POST",
//         url: '/allocate_battery/'+battery_pack_sr_no,
//         headers:{'X-CSRFToken': csrftoken},
//         data: {
            
//             "battery_pack_sr_no":battery_pack_sr_no,
//             "model_name":model_name
//         },
//         dataType: "json",
//         success: function (data) {  
//             if (data.messages){

//                 alert("successfully ");
//             }
//         },
        
//     });
// }


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
    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $("#updated_model_name").val(model_name)
    $("#updated_battery_pack_sr_no").val(battery_pack_sr_no)
    url='/update_battery/'+battery_pack_sr_no
    $.ajax({
        type: "POST",
        url: url,
        headers:{'X-CSRFToken': csrftoken},
        data: {
            
            "battery_pack_sr_no":battery_pack_sr_no,
        },
        // dataType: "json",
        success: function (data) {  
            alert("successfully Deleted")
        },
        
    });
}

function open_delete_modal(){
    var battery_serial_no = $(this).data("battery_serial_number");
    var model_name = $(this).data("model_name");
    var model_battery_serial_no = model_name +" "+battery_serial_no;
    $("#model_name").text(model_battery_serial_no);
    $("#model_name_msg").text(model_battery_serial_no);
    $("#delete_battery").data("model", battery_serial_no);
    bootstrap.Modal.getOrCreateInstance(document.getElementById("delete_modal")).show();
}


function moblisation(){
    var checkbox_status = $(this).is(":checked");
    var battery_pack_sr_no = $(this).data("battery_pack_sr_no");
    var status = $(this).data("status");
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    url = "/moblisation_status/"+battery_pack_sr_no+"/"
    $.ajax({
        type: "POST",
        url: url,
        headers:{'X-CSRFToken': csrftoken},
        data: {
            "status":status,
            "battery_pack_sr_no":battery_pack_sr_no,
            "checkbox_status":checkbox_status,
        },
        
        success: function (data) {  
            if(data.messages){

                $("#moblisation_status_text").text(data.messages);
                bootstrap.Modal.getOrCreateInstance(document.getElementById("moblisation_status_modal")).show();
            }
        },
        
    });

}

function refresh_status(){
    debugger;
    var battery_pack_sr_no = $(this).data("battery_pack_sr_no");
    url = "/refresh_status/"+battery_pack_sr_no+"/"
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        url: url,
        headers:{'X-CSRFToken': csrftoken},
        data: {
            "battery_pack_sr_no":battery_pack_sr_no,
        },
        
        success: function (data) {  
            if(data.messages){
                alert(data.messages);
            }
        },
        
    });

}

function change_icon(){
    $("#dashboad-tab").addClass("active-menu-icon-bg");
}

$("#battery-tab").on("click", function() {
    $(this).css("background", "red");
})

$(document).ready(function(){
    $("#hide_password").hide();
    // $(document).on("click", "#allocate_battery", allocate_battery_fun);
    $(document).on("click", "#delete_battery", delete_battery);
    $(document).on("click", "#update_battery", update_battery);
    $(document).on("click", "#show_password", password_show);
    $(document).on("click", "#hide_password", password_hide);
    $(document).on("click", "#delete_btn", open_delete_modal);
    $(document).on("click", "#moblisation_status", moblisation);
    $(document).on("click", ".refresh_btn", refresh_status);
    // $(document).on("click", "#battery-tab", change_icon);
    // $(document).on("click", "#dashboad-tab", change_icon); 
});