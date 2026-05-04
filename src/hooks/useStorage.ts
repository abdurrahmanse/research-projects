import { useState } from 'react';

/**
 * Hook for using localStorage with React state
 * @param key - Storage key
 * @param initialValue - Initial value if not in storage
 * @returns State value and setter
 */
export const useLocalStorage = <T,>(
    key: string,
    initialValue: T,
): [T, (value: T | ((val: T) => T)) => void] => {
    const [storedValue, setStoredValue] = useState<T>(() => {
        try {
            if (typeof window === 'undefined') {
                return initialValue;
            }

            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.error(`Error reading localStorage key "${key}":`, error);
            return initialValue;
        }
    });

    const setValue = (value: T | ((val: T) => T)) => {
        try {
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);

            if (typeof window !== 'undefined') {
                window.localStorage.setItem(key, JSON.stringify(valueToStore));
            }
        } catch (error) {
            console.error(`Error setting localStorage key "${key}":`, error);
        }
    };

    return [storedValue, setValue];
};

/**
 * Hook for using sessionStorage with React state
 * @param key - Storage key
 * @param initialValue - Initial value if not in storage
 * @returns State value and setter
 */
export const useSessionStorage = <T,>(
    key: string,
    initialValue: T,
): [T, (value: T | ((val: T) => T)) => void] => {
    const [storedValue, setStoredValue] = useState<T>(() => {
        try {
            if (typeof window === 'undefined') {
                return initialValue;
            }

            const item = window.sessionStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.error(`Error reading sessionStorage key "${key}":`, error);
            return initialValue;
        }
    });

    const setValue = (value: T | ((val: T) => T)) => {
        try {
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);

            if (typeof window !== 'undefined') {
                window.sessionStorage.setItem(key, JSON.stringify(valueToStore));
            }
        } catch (error) {
            console.error(`Error setting sessionStorage key "${key}":`, error);
        }
    };

    return [storedValue, setValue];
};

/**
 * Hook for clearing localStorage
 * @returns Function to clear all or specific keys
 */
export const useClearLocalStorage = () => {
    return (keys?: string[]) => {
        try {
            if (typeof window === 'undefined') return;

            if (keys) {
                keys.forEach((key) => window.localStorage.removeItem(key));
            } else {
                window.localStorage.clear();
            }
        } catch (error) {
            console.error('Error clearing localStorage:', error);
        }
    };
};

/**
 * Hook for removing a specific localStorage item
 * @param key - Storage key to remove
 */
export const useRemoveLocalStorageItem = () => {
    return (key: string) => {
        try {
            if (typeof window === 'undefined') return;
            window.localStorage.removeItem(key);
        } catch (error) {
            console.error(`Error removing localStorage key "${key}":`, error);
        }
    };
};
