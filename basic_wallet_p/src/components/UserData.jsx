import React from 'react';

export default function FormID ({user, balance, transactions}) {
  return (
    <>
      <h2>{user}'s Balance: {balance}</h2>
      <h2>{user}'s Transactions</h2>
      <ul>
        {transactions.map(trx => {
          return (
            <li key={trx.id} className="trx">
              <ul>
                <li>Transaction ID: {trx.id}</li>
                <li>Amount: {trx.amount}</li>
                <li>Sender: {trx.sender}</li>
                <li>Recipient: {trx.recipient}</li>
              </ul>
            </li>
          )
        })}
      </ul>
    </>
  )
}
