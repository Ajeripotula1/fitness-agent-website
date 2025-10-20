import React from 'react'

const TabButton = ({ tabId, label, isActive, onClick }) => {
  return (
    <button
        onClick={()=> {onClick(tabId)}}
        className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                isActive 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
        >
        {label}
    </button>
  )
}

export default TabButton