import type { Achievement } from '@/data';
import {
    achievements,
    getAchievementById,
    getAchievementCategories,
    getAchievementCountByYear,
    getAchievementIssuers,
    getAchievementsByCategory,
    getAchievementsByIssuer,
    getAchievementsSortedByDate,
    getFeaturedAchievements,
} from '@/data';

/**
 * Hook for accessing all achievements
 * @returns Array of all achievements
 */
export const useAchievements = (): Achievement[] => {
    return achievements;
};

/**
 * Hook for getting featured achievements
 * @returns Array of featured achievements
 */
export const useFeaturedAchievements = (): Achievement[] => {
    return getFeaturedAchievements();
};

/**
 * Hook for getting achievement by ID
 * @param id - Achievement ID
 * @returns Achievement or undefined
 */
export const useAchievementById = (id: string): Achievement | undefined => {
    return getAchievementById(id);
};

/**
 * Hook for filtering achievements by category
 * @param category - Achievement category
 * @returns Array of achievements in category
 */
export const useAchievementsByCategory = (category: string): Achievement[] => {
    return getAchievementsByCategory(category);
};

/**
 * Hook for filtering achievements by issuer
 * @param issuer - Issuer name
 * @returns Array of achievements from issuer
 */
export const useAchievementsByIssuer = (issuer: string): Achievement[] => {
    return getAchievementsByIssuer(issuer);
};

/**
 * Hook for getting achievements sorted by date (newest first)
 * @returns Array of achievements sorted by date
 */
export const useAchievementsSortedByDate = (): Achievement[] => {
    return getAchievementsSortedByDate();
};

/**
 * Hook for getting all achievement categories
 * @returns Array of unique categories
 */
export const useAchievementCategories = (): string[] => {
    return getAchievementCategories();
};

/**
 * Hook for getting all achievement issuers
 * @returns Array of unique issuer names
 */
export const useAchievementIssuers = (): string[] => {
    return getAchievementIssuers();
};

/**
 * Hook for getting achievement count by year
 * @returns Object with year as key and count as value
 */
export const useAchievementCountByYear = (): Record<string, number> => {
    return getAchievementCountByYear();
};

/**
 * Hook for getting featured achievement count
 * @returns Number of featured achievements
 */
export const useFeaturedAchievementCount = (): number => {
    return getFeaturedAchievements().length;
};

/**
 * Hook for getting total achievement count
 * @returns Total number of achievements
 */
export const useAchievementCount = (): number => {
    return achievements.length;
};
