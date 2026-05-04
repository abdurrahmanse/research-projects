import type { Statistic } from '@/data';
import {
    getAchievementStatistics,
    getAllStatistics,
    getCareerStatistics,
    getSocialStatistics,
    getStatisticById,
    getStatisticsWithTrends,
    statistics,
} from '@/data';

/**
 * Hook for accessing all statistics
 * @returns Array of all statistics
 */
export const useStatistics = (): Statistic[] => {
    return getAllStatistics();
};

/**
 * Hook for getting statistic by ID
 * @param id - Statistic ID
 * @returns Statistic or undefined
 */
export const useStatisticById = (id: string): Statistic | undefined => {
    return getStatisticById(id);
};

/**
 * Hook for getting career-related statistics
 * @returns Array of career statistics
 */
export const useCareerStatistics = (): Statistic[] => {
    return getCareerStatistics();
};

/**
 * Hook for getting social media statistics
 * @returns Array of social statistics
 */
export const useSocialStatistics = (): Statistic[] => {
    return getSocialStatistics();
};

/**
 * Hook for getting achievement-related statistics
 * @returns Array of achievement statistics
 */
export const useAchievementStatistics = (): Statistic[] => {
    return getAchievementStatistics();
};

/**
 * Hook for getting statistics with trends
 * @returns Array of statistics with trend indicators
 */
export const useStatisticsWithTrends = (): Statistic[] => {
    return getStatisticsWithTrends();
};

/**
 * Hook for getting specific numeric statistic value
 * @param id - Statistic ID
 * @returns Numeric value or undefined
 */
export const useStatisticValue = (id: string): number | undefined => {
    const stat = getStatisticById(id);
    return stat && typeof stat.value === 'number' ? stat.value : undefined;
};

/**
 * Hook for getting statistic count
 * @returns Total number of statistics
 */
export const useStatisticCount = (): number => {
    return statistics.length;
};

/**
 * Hook for getting statistics grouped by category
 * @returns Object with category as key and statistics array as value
 */
export const useStatisticsGrouped = (): Record<string, Statistic[]> => {
    return {
        career: getCareerStatistics(),
        social: getSocialStatistics(),
        achievement: getAchievementStatistics(),
    };
};
