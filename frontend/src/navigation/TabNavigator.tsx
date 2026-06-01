import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Home, Dumbbell, BarChart2, User } from 'lucide-react-native';

// מסכי דמי זמניים - נחליף אותם במסכים האמיתיים מיד בהמשך
import HomeScreen from '../screens/HomeScreen';
import WorkoutScreen from '../screens/WorkoutScreen';
import AnalyticsScreen from '../screens/AnalyticsScreen';
import ProfileScreen from '../screens/ProfileScreen';

const Tab = createBottomTabNavigator();

export const TabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#2563eb', // כחול כושר מודרני לטאב הפעיל
        tabBarInactiveTintColor: '#64748b', // אפור לטאבים הכבויים
        headerStyle: { backgroundColor: '#f8fafc' },
        headerTitleAlign: 'center',
      }}
    >
      <Tab.Screen 
        name="HomeTab" 
        component={HomeScreen} 
        options={{
          title: 'מסך הבית',
          tabBarLabel: 'בית',
          tabBarIcon: ({ color, size }) => <Home color={color} size={size} />,
        }}
      />
      <Tab.Screen 
        name="WorkoutTab" 
        component={WorkoutScreen} 
        options={{
          title: 'אימון פעיל',
          tabBarLabel: 'אימון',
          tabBarIcon: ({ color, size }) => <Dumbbell color={color} size={size} />,
        }}
      />
      <Tab.Screen 
        name="AnalyticsTab" 
        component={AnalyticsScreen} 
        options={{
          title: 'אנליטיקה וגרפים',
          tabBarLabel: 'גרפים',
          tabBarIcon: ({ color, size }) => <BarChart2 color={color} size={size} />,
        }}
      />
      <Tab.Screen 
        name="ProfileTab" 
        component={ProfileScreen} 
        options={{
          title: 'פרופיל ומעקב',
          tabBarLabel: 'פרופיל',
          tabBarIcon: ({ color, size }) => <User color={color} size={size} />,
        }}
      />
    </Tab.Navigator>
  );
};