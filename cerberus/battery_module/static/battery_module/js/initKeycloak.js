console.log("hi from init file")
var keycloak=new Keycloak('./battery_module/templates/battery_module/keycloak.json');
function initKeycloak() {
    keycloak.init({onLoad: 'login-required'}).then(function() {
    consol.log("hii am there")
    if(!localStorage.getItem("access_token")){
        localStorage.setItem("access_token", keycloak.token)
        console.log(keycloak.token)
    }
    }).catch(function() {
        alert('failed to initialize');
    });
        }
    initKeycloak();