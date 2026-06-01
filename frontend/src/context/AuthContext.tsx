import React, { createContext, useState, useEffect, useContext } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import apiClient from '../api/client';
import { User } from '../types';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (token: string, userData: User) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // בודק בכל הפעלה של האפליקציה אם המשתמש כבר מחובר (כדי שלא יצטרך לעשות לוגין כל פעם)
  useEffect(() => {
    const loadStorageData = async () => {
      try {
        const storedToken = await AsyncStorage.getItem('user_token');
        const storedUser = await AsyncStorage.getItem('user_data');

        if (storedToken && storedUser) {
          setToken(storedToken);
          setUser(JSON.parse(storedUser));
        }
      } catch (e) {
        console.error("Failed to load auth data from storage", e);
      } finally {
        setIsLoading(false);
      }
    };

    loadStorageData();
  }, []);

  // פונקציית התחברות מוצלחת
  const login = async (newToken: string, userData: User) => {
    setToken(newToken);
    setUser(userData);
    await AsyncStorage.setItem('user_token', newToken);
    await AsyncStorage.setItem('user_data', JSON.stringify(userData));
  };

  // פונקציית התנתקות (Logout)
  const logout = async () => {
    setToken(null);
    setUser(null);
    await AsyncStorage.removeItem('user_token');
    await AsyncStorage.removeItem('user_data');
  };

  return (
    <AuthContext.Provider value={{ user, token, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook מותאם אישית כדי למשוך את נתוני ה-Auth בקלות מכל מסך
export const useAuth = () => useContext(AuthContext);