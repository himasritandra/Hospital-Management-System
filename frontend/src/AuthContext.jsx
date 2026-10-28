import { createContext, useContext, useEffect, useState } from 'react';
import api from './api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function init() {
      try {
        await api.get('/csrf/');
        const res = await api.get('/me/');
        setUser(res.data);
      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
    }
    init();
  }, []);

  const login = async (username, password) => {
    const res = await api.post('/login/', { username, password });
    setUser(res.data);
    return res.data;
  };

  const register = async (data) => {
    const res = await api.post('/register/', data);
    setUser(res.data);
    return res.data;
  };

  const logout = async () => {
    await api.post('/logout/');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);