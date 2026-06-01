import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// 🛑 חובה: החלף את ה-IP הזה בכתובת ה-IP האמיתית של מחשב ה-Desktop שלך!
const COMPUTER_IP = '192.168.1.100'; 

const apiClient = axios.create({
  baseURL: `http://${COMPUTER_IP}:8000`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// מנגנון שמזריק אוטומטית את ה-JWT Token לכל קריאה שיוצאת מהסמסונג
apiClient.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('user_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;