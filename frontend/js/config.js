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
            // Production - AWS deployment
            // TODO: Replace with your actual AWS URL after deployment
            // Examples:
            // - ALB: 'https://your-alb-url.us-east-1.elb.amazonaws.com/api/v1'
            // - Domain: 'https://api.stacktutor.com/api/v1'
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
