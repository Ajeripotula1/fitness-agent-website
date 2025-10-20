const API_URL = import.meta.env.VITE_API_URL

//  Define all the Authfunctions we might need as dictionaries 
export const authService = {
    // In authService.js:
    register: async (username, password) => {
    console.log('🔍 Sending registration request:', { username, password });
    
    const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    
    console.log('🔍 Response status:', response.status);
    console.log('🔍 Response ok:', response.ok);
    
    if (!response.ok) {
        const errorData = await response.json();
        console.log('🔍 Error response:', errorData);
        
        // Handle specific error cases
        if (response.status === 409) {
            throw new Error('Username already taken. Please choose a different username.');
        } else if (response.status === 400) {
            throw new Error('Invalid registration data. Please check your input.');
        } else {
            throw new Error(errorData.detail || 'Registration failed. Please try again.');
        }
    }

    const result = await response.json();
    console.log('🔍 Success response:', result);
    return result;
},

    login: async (username, password) => {
        const response = await fetch(`${API_URL}/auth/token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, // data incoded into singe string (like URL query string)
            body: new URLSearchParams({ username, password })
        })
        if (!response.ok) {
            throw new Error('Login failed.');
        }

        return response.json() // return Token and user info 

    },

    getCurrentUser: async (token) => {
        const response = await fetch(`${API_URL}/auth/me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        if (!response.ok) {
            throw new Error('Failed to get current user');
        }
        return response.json()
    },
}