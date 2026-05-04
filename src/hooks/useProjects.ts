import type { Project } from '@/data';
import {
    getFeaturedProjects,
    getProjectById,
    getProjectsByCategory,
    getProjectsByTechnology,
    projects,
} from '@/data';

/**
 * Hook for accessing all projects
 * @returns Array of all projects
 */
export const useProjects = (): Project[] => {
    return projects;
};

/**
 * Hook for getting featured projects
 * @returns Array of featured projects (max 3)
 */
export const useFeaturedProjects = (): Project[] => {
    return getFeaturedProjects();
};

/**
 * Hook for getting project by ID
 * @param id - Project ID
 * @returns Project or undefined
 */
export const useProjectById = (id: string): Project | undefined => {
    return getProjectById(id);
};

/**
 * Hook for filtering projects by category
 * @param category - Project category
 * @returns Array of projects in category
 */
export const useProjectsByCategory = (category: string): Project[] => {
    return getProjectsByCategory(category);
};

/**
 * Hook for filtering projects by technology
 * @param technology - Technology name
 * @returns Array of projects using technology
 */
export const useProjectsByTechnology = (technology: string): Project[] => {
    return getProjectsByTechnology(technology);
};

/**
 * Hook for getting all project categories
 * @returns Array of unique categories
 */
export const useProjectCategories = (): string[] => {
    const categories = new Set<string>();
    projects.forEach((p) => categories.add(p.category));
    return Array.from(categories);
};

/**
 * Hook for getting all technologies used
 * @returns Array of unique technologies
 */
export const useProjectTechnologies = (): string[] => {
    const technologies = new Set<string>();
    projects.forEach((p) => {
        p.technologies.forEach((tech) => technologies.add(tech));
    });
    return Array.from(technologies);
};

/**
 * Hook for getting project count
 * @returns Total number of projects
 */
export const useProjectCount = (): number => {
    return projects.length;
};

/**
 * Hook for getting featured project count
 * @returns Number of featured projects
 */
export const useFeaturedProjectCount = (): number => {
    return getFeaturedProjects().length;
};
