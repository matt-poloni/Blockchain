import React, {useState, useEffect} from 'react';
import axios from 'axios';
import './App.css';

import UserInput from './components/UserInput';
import UserData from './components/UserData';

function App() {
  const [user, setUser] = useState('matt-poloni')
  const [bal, setBal] = useState(0)
  const [trx, setTrx] = useState([])

  const changeUser = e => setUser(e.target.value);

  useEffect(() => {
    axios
      .get(`http://localhost:5000/transactions/user/${user}`)
      .then(res => {
        const { balance, transactions } = res.data;
        setBal(balance);
        setTrx(transactions);
      });
  }, [user]);

  return (
    <div className="App">
      <UserInput
        user={user}
        handleChanges={changeUser}
      />
      <UserData
        user={user}
        balance={bal}
        transactions={trx}
      />
    </div>
  );
}

export default App;
