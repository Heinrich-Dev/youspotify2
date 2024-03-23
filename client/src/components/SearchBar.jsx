import {useEffect, useState, useRef} from 'react'

function SearchBar(){
    const [query, setQuery] = useState("")
    const inputRef = useRef()

    function OnSubmit(e) {
        e.preventDefault()
        const val = inputRef.current.value

        fetch("/youtubeget", {
            method: 'POST',
            body: JSON.stringify({
                "search": val
            }),
            headers: {
                'Content-type': 'application/json; charset=UTF-8'
            },
        })

        console.log()
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