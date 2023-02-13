function logout(){
    var access_token = localStorage.getItem("access_token")
    post_data = {"access_token":access_token}
    $.ajax({
            type: 'POST',
            url : "/logout/",
            success: function(response){
                console.log(response.messages);
            },
        });


    data = ajaxCall('/logout/', post_data).then((response)=>{

        alert("logout successfully")

    });
}

$(document).ready(function(){

    $(document).on("click", "#logout_btn", logout);
    
});