import React from 'react'
import CanvasMap from './CanvasMap'
import './App.css'

function App() {
  const [count, setCount] = React.useState(0)

  return (
    <>
      <div>
        <h1>AIM Machine Map</h1>
      </div>
      <div className="card">
        <button onClick={() => setCount(c => c + 1)}>
          Add machine
        </button>
      </div>
      <div className="card">
        <CanvasMap count={count} />
      </div>
    </>
  )
}

export default App
