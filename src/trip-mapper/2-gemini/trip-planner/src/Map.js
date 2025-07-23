import React from 'react';
import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';
import './Map.css';

const geoUrl = "https://raw.githubusercontent.com/deldersveld/topojson/master/world-countries.json";

const Map = ({ markers }) => {
  return (
    <div className="map-container">
      <ComposableMap
        projection="geoMercator"
        projectionConfig={{
          scale: 150
        }}
        width={800}
        height={450}
      >
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map(geo => (
              <Geography key={geo.rsmKey} geography={geo} fill="#EAEAEC" stroke="#D6D6DA" />
            ))
          }
        </Geographies>
        {markers.map(({ name, coordinates }) => (
          <Marker key={name} coordinates={coordinates}>
            <circle r={8} fill="#F53" />
            <text
              textAnchor="middle"
              y={-15}
              style={{ fontFamily: "system-ui", fill: "#5D5A6D", fontSize: "12px" }}
            >
              {name}
            </text>
          </Marker>
        ))}
      </ComposableMap>
    </div>
  );
};

export default Map;