// oidcConfig.js
export const oidcConfig = {
  authority: "http://localhost:8082/realms/hypertube",
  client_id: "web",
  redirect_uri: window.location.origin + "/callback",
  post_logout_redirect_uri: window.location.origin,
  response_type: "code",
  scope: "openid profile email",
  automaticSilentRenew: true,  // auto-refresh tokens
  loadUserInfo: true
};

// example of oidc integration with SPA frontend (based on REACT)