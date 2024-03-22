import React from 'react'

function Button() {
    const handleClick = (e) => {
        e.preventDefault();
        alert("Clicked!");
    }
    return (
        <button onClick={handleClick}>
            Click Me
        </button>
    )
}
export default Button