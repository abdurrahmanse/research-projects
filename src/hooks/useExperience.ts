import type { WorkExperience } from '@/data';
import { calculateTotalExperience, getCurrentWork, getWorkExperienceById, workExperience } from '@/data';

/**
 * Hook for accessing all work experience
 * @returns Array of work experience records
 */
export const useExperience = (): WorkExperience[] => {
    return workExperience;
};

/**
 * Hook for getting current work position
 * @returns Current work experience or undefined
 */
export const useCurrentWork = (): WorkExperience | undefined => {
    return getCurrentWork();
};

/**
 * Hook for getting total years of experience
 * @returns Total years as number
 */
export const useTotalExperience = (): number => {
    return calculateTotalExperience();
};

/**
 * Hook for getting work experience by ID
 * @param id - Work experience ID
 * @returns Work experience or undefined
 */
export const useWorkExperienceById = (id: string): WorkExperience | undefined => {
    return getWorkExperienceById(id);
};

/**
 * Hook for getting all companies worked for
 * @returns Array of company names
 */
export const useCompanies = (): string[] => {
    return workExperience.map((exp) => exp.company);
};
