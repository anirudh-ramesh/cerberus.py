var keycloak=new Keycloak('http://localhost:5500/keycloak.json');
    function initKeycloak() {
        // new Keycloak('http://cerberus.localhost/keycloak.json');
        console.log("hii am there")    
        keycloak.init({onLoad: 'login-required'}).then(function() {
            // constructTableRows(keycloak.idTokenParsed);
            // pasteToken(keycloak.token);
        }).catch(function() {
            alert('failed to initialize');
        });
         }
        initKeycloak();
        console.log("Print my name !!") 