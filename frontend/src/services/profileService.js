const API_URL = import.meta.env.VITE_API_URL

export const profileService = {

    createProfile: async (profileData, token) => {
        const response = await fetch(`${API_URL}/profile/`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(profileData) //conver JS obj into JSON string
        })
        if (!response.ok) {
            const error = await response.json(); // convert JSON string to js obj
            throw new Error(error.detail || 'Failed to create profile');
        }
        return response.json();
    },

    getProfile: async (token) => {
        const response = await fetch(`${API_URL}/profile/`, {
            method: "GET",
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        if (!response.ok) {
            if (response.status === 404) {
                return null
            }
            throw new Error('Failed to get profile')
        }
        return response.json()
    }
}