import { createContext, useContext, useEffect, useState } from "react";
import { authService } from '../services/authService'
// CREATE CONTEXT - "storage box" / global state
const AuthContext = createContext();
//  PROVIDER COMPONENT - manages the global state

// Wraps around application to provide application context to its child components 
function AuthProvider({ children }) {

    useEffect(() => {
        const initializeAuth = async () => {
            const savedToken = localStorage.getItem('token')
            console.log("Running Effect")
            if (savedToken) {
                setToken(savedToken)
                try {
                    // Verify token and get user info
                    const userData = await authService.getCurrentUser(savedToken)
                    setUser(userData)
                } catch (error) {
                    // Token is invalid, remove it
                    console.error('Token validation failed:', error)
                    localStorage.removeItem('token')
                    setToken(null)
                }
            }
            setIsLoading(false);
        }
        
        initializeAuth()
    }, [])

    // globally shared state that components may need to know
    const [user, setUser] = useState(null)
    const [token, setToken] = useState(null)
    const [isLoading, setIsLoading] = useState(true)

    const registerUser = async (username, password) => {
        try {
            setIsLoading(true)
            const result = await authService.register(username, password)

            // On Success, issue token and auto login user
            setToken(result.access_token)
            setUser({ username })
            // Save token to local storage
            localStorage.setItem('token', result.access_token)

        } catch (error) {
            console.error('Registration failed:', error);
            throw error;
        } finally {
            setIsLoading(false);
        }
    }
    const loginUser = async (username, password) => {
        try {
            setIsLoading(true)
            // Call login service function w/ user name and password
            const result = await authService.login(username, password)

            // Update states
            setToken(result.access_token)
            setUser({ username });

            // Save token to local storage
            localStorage.setItem('token', result.access_token)
        }
        catch (error) {
            console.error('Login failed:', error)
            throw error
        }
        finally {
            setIsLoading(false)
        }
    }
    const logout = async () => {
        setUser(null)
        setToken(null)
        localStorage.removeItem('token')

    }

    // what "value" will be shared with all components
    // what data do we need to track globally? 
    const value = {
        user, // current user info from auth/me
        token, // jwt tokens for protected API calls 
        isAuthenticated: !!user,
        isLoading, // are we checking auth status? 
        register: registerUser, // create account
        login: loginUser, // call API and save token
        logout, // clear token and redirect
        // register // create account
    }
    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )
}

// Define CUSTOM HOOK - easy way for components to use the context
// Access thhe authentication context from whith components  
function useAuth() {
    const context = useContext(AuthContext)
    if (!context) {
        throw new Error('userAuth must be used within AuthProvider')
    }
    return context;
}

export { AuthProvider, useAuth }