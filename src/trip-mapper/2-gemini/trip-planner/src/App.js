import React, { useState } from 'react';
import Map from './Map';
import Itinerary from './Itinerary';
import './App.css';

function App() {
  const mockTrips = [
    {
      location: { name: "Paris, France", coordinates: [2.3522, 48.8566] },
      itinerary: [
        {
          day: 1,
          location: "Paris, France",
          activities: [
            { time: "9:00 AM", description: "Visit the Eiffel Tower" },
            { time: "1:00 PM", description: "Lunch at a local bistro" },
            { time: "3:00 PM", description: "Explore the Louvre Museum" },
          ],
        },
        {
          day: 2,
          location: "Paris, France",
          activities: [
            { time: "10:00 AM", description: "Stroll along the Seine River" },
            { time: "12:00 PM", description: "Picnic in Luxembourg Gardens" },
            { time: "4:00 PM", description: "Discover Montmartre and Sacré-Cœur" },
          ],
        },
        {
          day: 3,
          location: "Paris, France",
          activities: [
            { time: "9:30 AM", description: "Enjoy a croissant and coffee" },
            { time: "11:00 AM", description: "Shopping on Champs-Élysées" },
            { time: "2:00 PM", description: "Depart from Paris" },
          ],
        },
      ],
    },
    {
      location: { name: "Tokyo, Japan", coordinates: [139.6917, 35.6895] },
      itinerary: [
        {
          day: 1,
          location: "Tokyo, Japan",
          activities: [
            { time: "9:00 AM", description: "Visit the Senso-ji Temple" },
            { time: "1:00 PM", description: "Lunch in Shibuya" },
            { time: "3:00 PM", description: "Explore the Meiji Jingu Shrine" },
          ],
        },
        {
          day: 2,
          location: "Tokyo, Japan",
          activities: [
            { time: "10:00 AM", description: "Experience the Tsukiji Outer Market" },
            { time: "12:00 PM", description: "Walk through Shinjuku Gyoen National Garden" },
            { time: "4:00 PM", description: "Enjoy the view from Tokyo Skytree" },
          ],
        },
        {
          day: 3,
          location: "Tokyo, Japan",
          activities: [
            { time: "9:30 AM", description: "Visit the Imperial Palace East Garden" },
            { time: "11:00 AM", description: "Shopping in Ginza" },
            { time: "2:00 PM", description: "Depart from Tokyo" },
          ],
        },
      ],
    },
    {
      location: { name: "Rio de Janeiro, Brazil", coordinates: [-43.1729, -22.9068] },
      itinerary: [
        {
          day: 1,
          location: "Rio de Janeiro, Brazil",
          activities: [
            { time: "9:00 AM", description: "Visit Christ the Redeemer" },
            { time: "1:00 PM", description: "Lunch at a churrascaria" },
            { time: "3:00 PM", description: "Relax on Copacabana Beach" },
          ],
        },
        {
          day: 2,
          location: "Rio de Janeiro, Brazil",
          activities: [
            { time: "10:00 AM", description: "Take a cable car to Sugarloaf Mountain" },
            { time: "12:00 PM", description: "Explore the Santa Teresa neighborhood" },
            { time: "4:00 PM", description: "Enjoy sunset at Arpoador" },
          ],
        },
        {
          day: 3,
          location: "Rio de Janeiro, Brazil",
          activities: [
            { time: "9:30 AM", description: "Visit the Selarón Steps" },
            { time: "11:00 AM", description: "Explore the Botanical Garden" },
            { time: "2:00 PM", description: "Depart from Rio" },
          ],
        },
      ],
    },
  ];

  const [currentTrip, setCurrentTrip] = useState(mockTrips[0]);

  const handleRandomize = () => {
    const randomIndex = Math.floor(Math.random() * mockTrips.length);
    setCurrentTrip(mockTrips[randomIndex]);
  };

  const itinerary = currentTrip.itinerary;
  const markers = [currentTrip.location];

  return (
    <div className="App">
      <header className="App-header">
        <h1>Trip Planner</h1>
        <button onClick={handleRandomize}>Randomize Trip</button>
      </header>
      <div className="main-content">
        <div className="map-section">
          <Map markers={markers} />
        </div>
        <div className="itinerary-section">
          <Itinerary itinerary={itinerary} />
        </div>
      </div>
    </div>
  );
}

export default App;
