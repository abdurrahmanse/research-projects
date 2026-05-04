import type { SkillCategory, SoftSkill } from '@/data';
import {
    getAllTechnicalSkills,
    getExpertSkills,
    getSkillsByCategory,
    getSkillsByProficiency,
    getTotalEndorsements,
    softSkills,
    technicalSkills,
} from '@/data';

/**
 * Hook for accessing all technical skills
 * @returns Array of technical skill categories
 */
export const useTechnicalSkills = (): SkillCategory[] => {
    return technicalSkills;
};

/**
 * Hook for accessing all soft skills
 * @returns Array of soft skills
 */
export const useSoftSkills = (): SoftSkill[] => {
    return softSkills;
};

/**
 * Hook for getting all technical skill names
 * @returns Array of skill names
 */
export const useAllTechnicalSkillNames = (): string[] => {
    return getAllTechnicalSkills();
};

/**
 * Hook for getting skills by category
 * @param category - Skill category name
 * @returns Array of skill names in category
 */
export const useSkillsByCategory = (category: string): string[] => {
    return getSkillsByCategory(category);
};

/**
 * Hook for getting expert-level skills
 * @returns Array of expert-level skill names
 */
export const useExpertSkills = (): string[] => {
    return getExpertSkills();
};

/**
 * Hook for getting skills by proficiency level
 * @param proficiency - Proficiency level
 * @returns Array of skill names
 */
export const useSkillsByProficiency = (proficiency: 'Beginner' | 'Intermediate' | 'Advanced' | 'Expert'): string[] => {
    return getSkillsByProficiency(proficiency);
};

/**
 * Hook for getting total endorsements
 * @returns Total endorsement count
 */
export const useTotalEndorsements = (): number => {
    return getTotalEndorsements();
};

/**
 * Hook for getting all skill categories
 * @returns Array of category names
 */
export const useSkillCategories = (): string[] => {
    return technicalSkills.map((cat) => cat.category);
};
