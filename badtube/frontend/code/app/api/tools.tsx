export function get_url(endpoint: string): string {
    return "http://localhost:8000" + endpoint;
    // return window.location.origin + endpoint;
}
