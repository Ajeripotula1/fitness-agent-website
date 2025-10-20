const API_URL = import.meta.env.VITE_API_URL

export const planService = {
    generatePlan: async (token) => {
        // GET request to /agent/generate-plan
        const response = await fetch(`${API_URL}/agent/generate-plan`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` } // Include Authorization header
        })
        if (!response.ok) {
            throw new Error('Could not retrieve Plan.');
        }
        return response.json() // convert JSON string to js obj
    },

    getPlan: async (token) => {
        // GET request to the /get-plan endpoints
        const response = await fetch(`${API_URL}/agent/get-plan`, {
            "method" : "GET",
            "headers" : { "Authorization": `Bearer ${token}` }
        })
        if (!response) {
            if (response.status === 404) {
                return null
            }
            throw new Error('Failed to get plan')
        }
        return response.json()
        
    },
   
}