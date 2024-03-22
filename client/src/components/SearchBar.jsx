import {useEffect, useState, useRef} from 'react'

function SearchBar(){
    const [query, setQuery] = useState("")
    const inputRef = useRef()

    function OnSubmit(e) {
        e.preventDefault()
        const value = inputRef.current.value
        
        var jsonData = {
            "search": value
        }

        fetch("/youtubeget", {
            method: 'POST',
            body: JSON.stringify(jsonData)
        })
    }
    
    return (
        <>
            <form onSubmit={OnSubmit}>
                <input ref={inputRef} type="text" />
                <button type="submit">Search</button>
            </form>
        </>
    )
}

export default SearchBar