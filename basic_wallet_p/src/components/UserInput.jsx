import React from 'react';

export default function UserInput ({user, handleChanges}) {
  const handleSubmit = e => {
    e.preventDefault()
  };

  return (
    <form onSubmit={handleSubmit}>
      <label for="input-user">User: </label>
      <input
        id="input-user"
        type="text"
        value={user}
        onChange={handleChanges}
      />
    </form>
  )
}
