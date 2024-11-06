import React, { useState } from 'react';
import './App.css';
import messages from './messages';

function App() {
  const [email, setEmail] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:5001/petition', {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain',
        },
        body: email,
      });

      const result = await response.json();
      if (response.ok) {
        alert('תודה שחתמת על העצומה!');
      } else {
        alert('שגיאה: ' + result.message);
      }
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  return (
    <div className="App" style={{ direction: "rtl" }}>
      <header>
        <h1>ועדת חקירה ממלכתית עכשיו!</h1>
      </header>
      <main>
        <p dangerouslySetInnerHTML={{ __html: messages.paragraph }}/>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="email">מייל: </label>
            <input
              type="email"
              id="email"
              name="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
            />
          </div>
          <button type="submit">שגר</button>
        </form>
      </main>
    </div>
  );
}

export default App;
