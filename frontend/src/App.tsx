import React, { useState, useEffect } from 'react';

function App() {
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/activities/list')
      .then(res => res.json())
      .then(data => setActivities(data.activities));
  }, []);

  return (
    <div>
      <h1>StepSight</h1>
      <div>
        {activities.map((activity: any) => (
          <div key={activity.id} style={{ border: '1px solid #ccc', margin: '10px', padding: '10px' }}>
            <h3>{activity.name}</h3>
            <p>Type: {activity.type}</p>
            <p>Date: {activity.date}</p>
            <p>Distance: {activity.distance}m</p>
            <p>Time: {activity.elapsed_time}s</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
