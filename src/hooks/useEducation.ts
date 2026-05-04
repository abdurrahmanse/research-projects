import type { Education } from '@/data';
import {
    education,
    getAllCourseworks,
    getCompletedEducation,
    getEducationById,
    getHighestDegree,
    getOngoingEducation,
} from '@/data';

/**
 * Hook for accessing all education records
 * @returns Array of education records
 */
export const useEducation = (): Education[] => {
    return education;
};

/**
 * Hook for getting completed education only
 * @returns Array of completed education
 */
export const useCompletedEducation = (): Education[] => {
    return getCompletedEducation();
};

/**
 * Hook for getting ongoing education
 * @returns Array of ongoing education
 */
export const useOngoingEducation = (): Education[] => {
    return getOngoingEducation();
};

/**
 * Hook for getting highest degree
 * @returns Highest education record or undefined
 */
export const useHighestDegree = (): Education | undefined => {
    return getHighestDegree();
};

/**
 * Hook for getting all courseworks across degrees
 * @returns Array of unique courseworks
 */
export const useAllCourseworks = (): string[] => {
    return getAllCourseworks();
};

/**
 * Hook for getting education by ID
 * @param id - Education ID
 * @returns Education record or undefined
 */
export const useEducationById = (id: string): Education | undefined => {
    return getEducationById(id);
};
