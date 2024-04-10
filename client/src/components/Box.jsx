import {useEffect, useState} from 'react'

function Box(){
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    useEffect(() => {
        fetch("/test")
        .then(response => response.json())
        .then(data => {
            setData(data);
            setLoading(false);
        })
        .catch(error => {
            setError(error);
            setLoading(false);
        })
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <div class="box"><p>{error.message}</p></div>

    if (data) {
        return <div class="box">{data.test}</div>
    } else {
        return <div class="box"> <p>No data found!</p></div>
    }
}

export default Box;