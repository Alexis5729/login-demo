export const msalConfig = {
    auth: {
        clientId: "8b7ff0a7-52a6-4dd6-b6ae-4cb04b551f28",

        authority:
            "https://login.microsoftonline.com/TU_TENANT/36e4a89a-590a-43c7-b9f3-3af8fffde2a0",

        redirectUri: "http://localhost:3000/"
    },

    cache: {
        cacheLocation: "sessionStorage"
    }
};

export const loginRequest = {
    scopes: ["openid", "profile", "email"]
};
