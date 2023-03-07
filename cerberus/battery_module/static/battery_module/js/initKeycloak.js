var keycloak = new Keycloak();

function initKeycloak() {
    keycloak.init({onLoad: 'login-required'}).then(function() {
        constructTableRows(keycloak.idTokenParsed);
        pasteToken(keycloak.token);
        console.log("dddddddd",keycloak.token)
    }).catch(function() {
        alert('failed to initialize');
    });
}