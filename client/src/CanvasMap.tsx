import React from 'react'
import { GoogleMap, useJsApiLoader } from '@react-google-maps/api'

const containerStyle = {
  width: '400px',
  height: '400px',
}

// Boston!
const center = {
  lat: 42.356,
  lng: 71.057,
}

type Props = {
  count: number;
};

function CanvasMap({ count }: Props) {
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: 'YOUR_API_KEY',
  })

  const [map, setMap] = React.useState(null)

  const onLoad = React.useCallback(function callback(m) {
    // This is just an example of getting and using the map instance!!! don't just blindly copy!
    const bounds = new window.google.maps.LatLngBounds(center)
    m.fitBounds(bounds)

    setMap(m)
  }, [])

  const onUnmount = React.useCallback(function callback(m) {
    setMap(null)
  }, [])

  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={10}
      onLoad={onLoad}
      onUnmount={onUnmount}
    >
      {/* Child components, such as markers, info windows, etc. */}
      <></>
    </GoogleMap>
  ) : (
    <></>
  )
}

export default React.memo(CanvasMap)