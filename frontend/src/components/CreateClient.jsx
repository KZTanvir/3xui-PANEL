import React, { useState } from 'react';
import { useAppContext } from '../ContextProvider';
import backend_url from './urls';
import axios from 'axios';

const CreateClient = () => {
  const { interfaces } = useAppContext();
  const [selectedInbound, setSelectedInbound] = useState('');
  const [username, setUsername] = useState('');
  const [responseMsg, setResponseMsg] = useState(null);

  const interfaceUrl = backend_url + '/create_client'

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = {
      'inbound_id': selectedInbound,
      'client_name': username
    }
    axios.post(interfaceUrl, {...payload})
      .then((response) => {
        setResponseMsg(response.data.msg)
      })
      .catch((error) => {
        console.log('something went wrong', error)
        setResponseMsg(null)
      })
  };
  return (
    <div className='card'>
      <h2 className='title'>Create Client</h2>
      <form onSubmit={handleSubmit} className='form-content'>
        <div className='form-group'>
          <label>Select Inbound:</label>
          <select
            value={selectedInbound}
            onChange={(e) => setSelectedInbound(e.target.value)}
            required
          >
            <option value="">Select Inbound</option>
            {interfaces.map((inbound) => (
              <option key={inbound.id} value={inbound.id}>
                {inbound.remark}
              </option>
            ))}
          </select>
        </div>

        <div className='form-group'>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <button type="submit">Create Client</button>
      </form>
      <p style={{color: 'red'}}>{responseMsg}</p>
    </div>
  );
};

export default CreateClient;
