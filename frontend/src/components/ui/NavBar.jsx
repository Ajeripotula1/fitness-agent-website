import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

const NavBar = () => {
    const navigate = useNavigate()
    const location = useLocation()
    const { logout } = useAuth()

    // Helper function to check if current route is active
    const isActive = (path) => location.pathname === path

    // Navigation items
    const navItems = [
        { path: '/home', label: 'Profile' },
        { path: '/plan', label: 'My Plan' }
    ]

    return (
        <nav className="bg-white shadow-sm border-b border-gray-200">
            <div className="max-w-4xl mx-auto px-4 md:px-6">
                <div className="flex justify-between items-center h-16">
                    
                    {/* Logo/Brand */}
                    <div className="flex items-center">
                        <h1 className="text-xl md:text-2xl font-bold text-gray-900">
                            FitAgent
                        </h1>
                    </div>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center space-x-8">
                        {navItems.map(item => (
                            <button
                                key={item.path}
                                onClick={() => navigate(item.path)}
                                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                                    isActive(item.path)
                                        ? 'text-blue-600 bg-blue-50'
                                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                                }`}
                            >
                                {item.label}
                            </button>
                        ))}
                        
                        <button
                            onClick={logout}
                            className="text-red-600 hover:text-red-700 hover:bg-red-50 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                        >
                            Logout
                        </button>
                    </div>

                    {/* Mobile Menu Button */}
                    <div className="md:hidden">
                        <button
                            onClick={() => {
                                // Toggle mobile menu (you can add state for this)
                                console.log('Mobile menu toggle')
                            }}
                            className="text-gray-600 hover:text-gray-900 p-2"
                        >
                            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                            </svg>
                        </button>
                    </div>
                </div>

                {/* Mobile Navigation (you can add state to show/hide this) */}
                <div className="md:hidden border-t border-gray-200 py-2">
                    {navItems.map(item => (
                        <button
                            key={item.path}
                            onClick={() => navigate(item.path)}
                            className={`block w-full text-left px-3 py-2 rounded-md text-base font-medium transition-colors ${
                                isActive(item.path)
                                    ? 'text-blue-600 bg-blue-50'
                                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                            }`}
                        >
                            {item.label}
                        </button>
                    ))}
                    
                    <button
                        onClick={logout}
                        className="block w-full text-left text-red-600 hover:text-red-700 hover:bg-red-50 px-3 py-2 rounded-md text-base font-medium transition-colors mt-2 border-t border-gray-200 pt-4"
                    >
                        Logout
                    </button>
                </div>
            </div>
        </nav>
    )
}

export default NavBar
