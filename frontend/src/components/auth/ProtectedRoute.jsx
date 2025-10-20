import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

const ProtectedRoute = ({ children }) => {
    const { isAuthenticated, isLoading} = useAuth()
    
    if(isLoading) {
        return <div>Loading...</div>
    }
    // Redirect to Login if not authenticated 
    if (!isAuthenticated) {
        return <Navigate to='/login' replace/>
    }
    // show protected cotnent if authenticated
    return children
};

export default ProtectedRoute