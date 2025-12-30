/**
 * API Configuration
 * Automatically detects environment and uses appropriate API URL
 */

const config = {
    // Detect if we're running locally or in production
    getApiUrl() {
        // Check if we're on localhost
        const hostname = window.location.hostname;
        const protocol = window.location.protocol;
        
        // If opened via file:// or localhost, use local API
        if (protocol === 'file:' || hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '') {
            // Development - local Docker
            return 'http://localhost:8001/api/v1';
        } else {
            // Production - prefer same-origin API (works when UI and API share a domain)
            if (window.location.origin && window.location.origin !== 'null') {
                return `${window.location.origin.replace(/\/$/, '')}/api/v1`;
            }
            // Fallback: set your API origin explicitly
            return 'https://YOUR_AWS_URL_HERE/api/v1';
        }
    },
    
    // Get the full API URL
    get API_URL() {
        return this.getApiUrl();
    }
};

// Log current configuration (helps with debugging)
console.log('API Configuration:', config.API_URL);
