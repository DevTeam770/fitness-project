import React from 'react';
import { View, ActivityIndicator } from 'react-native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useAuth } from '../context/AuthContext';

import LoginScreen from '../screens/LoginScreen';
import { TabNavigator } from './TabNavigator';

const Stack = createNativeStackNavigator();

export const AppNavigator = () => {
  const { user, isLoading } = useAuth();

  // בזמן שהאפליקציה בודקת בזיכרון של הסמסונג אם יש טוקן שמור - נציג מסך טעינה
  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#ffffff' }}>
        <ActivityIndicator size="large" color="#2563eb" />
      </View>
    );
  }

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {user ? (
        // 🔐 משתמש מחובר -> מקבל גישה לכל הטאבים של האפליקציה
        <Stack.Screen name="Main" component={TabNavigator} />
      ) : (
        // 🔓 משתמש אנונימי -> רואה רק את מסך ההתחברות
        <Stack.Screen name="Login" component={LoginScreen} />
      )}
    </Stack.Navigator>
  );
};