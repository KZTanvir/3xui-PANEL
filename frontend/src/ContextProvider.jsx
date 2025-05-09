import React, { useContext } from 'react'
import axios from 'axios';
import backend_url from './components/urls'
const appContext = React.createContext();

const ContextProvider = (props) => {
    const [interfaces, setInterfaces] = React.useState([])
    const [loading, setLoading] = React.useState(true)
    
    const interfacesUrl = backend_url + '/interface_list';
    const getInterfaces = () => {
        axios.get(interfacesUrl)
            .then((response) => {
                setInterfaces(response.data);
                setLoading(false)
            })
            .catch((error) => {
                console.log('something went wrong', error);
                setLoading(true);
            })
    }

    React.useEffect(() => {
        getInterfaces();
    }, [])
    return <appContext.Provider value={{interfaces, setInterfaces, loading}}>
        {props.children}
    </appContext.Provider>
}


const useAppContext = () => {
    return useContext(appContext)
}

export  {ContextProvider, useAppContext }