import React, { useEffect } from 'react'
import axios from 'axios';
import backend_url from './urls';
import { useAppContext } from '../ContextProvider';

const Interfaces = () => {
    const { interfaces, setInterfaces, loading } = useAppContext();
    const [showClients, setShowClients] = React.useState({});

    const to_speed = (value) => {
        if (value < 0) return 0;
        else return Math.floor(value / (1024 * 1024 * 1024));
    }

    const to_date = (value) => {
        const currentTime = Date.now();
        if (value <= currentTime) return 0;
        const daysRemaining = (value - currentTime) / (1000 * 60 * 60 * 24)
        return Math.floor(daysRemaining);
    }
    function to_json(json_sting) {
        return JSON.parse(json_sting)
    }
    const CurrentClient = (id) => {
        setShowClients((prev) => {
            return { ...prev, [id]: !prev[id] }
        })
    }
    function clientSettings(settings, client_name) {
        settings = to_json(settings)
        console.log(settings.clients)
        return settings.clients.find(client => client.email === client_name)
    }

    return <section>
        <div className='card'>
            <h2 className='title'>All Interfaces</h2>
            <hr />
        </div>
        {loading ? <p>loading</p> : interfaces.map((value, index) => {
            return <div key={index} className='card'>
                <div className='table-content'>
                    <p className='title'>{value.remark}</p>
                    <table className='table'>
                        <tbody>
                            <tr>
                                <td>ID</td>
                                <td>{value.id}</td>
                                <td>State</td>
                                <td>{value.enable ? 'Active' : 'Disabled'}</td>
                            </tr>
                            <tr>
                                <td>Uploads</td>
                                <td>{to_speed(value.up)} GB</td>
                                <td>Downloads</td>
                                <td>{to_speed(value.down)} GB</td>
                            </tr>
                            <tr>
                                <td>PORT</td>
                                <td>{value.port}</td>
                                <td>Protocol</td>
                                <td>{value.protocol}</td>
                            </tr>
                        </tbody>
                    </table>
                    <button onClick={() => CurrentClient(value.id)}>{showClients[value.id] ? 'Hide' : 'Show'}</button>
                </div>
                <div className="table-content">
                    {showClients[value.id] && <table className="table">
                        <thead>
                            <tr>
                                <th>Client</th>
                                <th>active</th>
                                <th>expiry</th>
                                <th>download </th>
                                <th>upload </th>
                                <th>limit</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {value.clientStats.map((client, index) => {
                                const client_settings = clientSettings(value.settings, client.email)

                                return <>
                                <tr>
                                    <td>{client.email}</td>
                                    <td>{client_settings.enable == 1 ? 'Active' : 'Disabled'}</td>
                                    <td>{to_date(client.expiryTime)}</td>
                                    <td>{to_speed(client.down)} GB</td>
                                    <td>{to_speed(client.up)} GB</td>
                                    <td>{to_speed(client.total)} GB</td>
                                    <td>
                                        <a href={"https://www.google.com/" + client.id}>
                                            <button>COPY</button>
                                        </a>
                                    </td>
                                </tr>
                                <tr>
                                    <td>{client.email} (id)</td>
                                    <td colSpan={5}>{client_settings.id}</td>
                                </tr>
                                </>
                            })}
                        </tbody>
                    </table>}
                </div>
            </div>
        })}
    </section>
}

export default Interfaces