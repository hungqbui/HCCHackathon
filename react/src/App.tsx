import { useEffect, useState } from 'react'
import './App.css'

import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";


import axios from 'axios'

function App() {

  const [url, setUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<any>()
  const [description, setDescription] = useState<any>()
  const [error, setError] = useState(false)
  const [latitude, setLatitude] = useState<any>()
  const [longitude, setLongitude] = useState<any>()
  const [city, setCity] = useState<any>()
  const [state, setState] = useState<any>()

  useEffect(() => {
    setIsLoading(true)
    navigator.geolocation.getCurrentPosition((pos) => {
      const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${pos.coords.latitude}&lon=${pos.coords.longitude}`

      axios.get(url).then((response) => {
        if ("village" in response.data.address) {
          setCity(response.data.address.village)
        } else if ("town" in response.data.address) {
          setCity(response.data.address.town)
        } else {
          setCity(response.data.address.city)
        }
        setState(response.data.address.state)
        setIsLoading(false)
      })
      
    })
    

  }, [])

  const handleSubmit = async (e: any) => {
    e.preventDefault()

    setIsLoading(true)
    setError(false)
    const response = await axios.post('http://localhost:5000/api', {
      "url": url,
      "city": city,
      "state": state
    })

    setResult(response.data)
    setDescription(JSON.parse(response.data.description))
    setIsLoading(false)

    console.log(description)

    if (!response.data.ok) {
      setError(true)
      return
    }

    console.log(response.data)
  }

  return (
    <> 
      <h1 id="title">Know Your Cuisine</h1>
      <div style={{ display: "flex", flexDirection: "column" }}>
        <div id="warning">{ error && result.error }</div>
        <form onSubmit={handleSubmit} id="form">
          <TextField InputLabelProps={{ style: { color: "white" } }} InputProps={{ style: { color: "white"} }} onChange={(e) => { setUrl(e.target.value) }} style={{ color: "white" }} id="text-field" variant="filled" label="Enter your image URL" />
          <Button disabled={isLoading} id="submit-btn" variant="contained" color="primary" onClick={handleSubmit}>
            Submit
          </Button>
        </form>
        <div style={{ display: "flex", justifyContent: "center" }}>
          { isLoading &&
          <img src={url} alt="input-image" id="input-image" style={{ marginTop: "20px" }} />
          }
        </div>
        {
          !error && result && !isLoading &&
          <div id="output-container">
            <img src={result.image} alt="input-image" id="input-image" />

            <caption><i>{description.name} from {description.origin}</i></caption>
            <p id="description">{description.description}</p>
            <div>
              <h2>More Infomation about {description.name}</h2>
              <div>
                
                <ul>
                { result.search_res.map((res : any) => {
                  return (
                    <li>
                      <a href={res}>{res}</a>
                    </li>
                  )
                }) }
                </ul>
              </div>
            </div>
          </div>
          
        }
      </div>
    </>
  )
}

export default App
