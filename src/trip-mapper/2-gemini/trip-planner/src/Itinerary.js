import React from 'react';
import './Itinerary.css';

const Itinerary = ({ itinerary }) => {
  return (
    <div className="itinerary-container">
      <h2>Your 3-Day Itinerary</h2>
      {itinerary.map((day, index) => (
        <div key={index} className="day-container">
          <h3>Day {day.day}: {day.location}</h3>
          <ul>
            {day.activities.map((activity, activityIndex) => (
              <li key={activityIndex}>
                <strong>{activity.time}</strong>: {activity.description}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default Itinerary;