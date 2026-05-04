import type { Service } from '@/data';
import {
    getFeaturedServices,
    getServiceById,
    getServicesByCategory,
    getServicesByTechnology,
    services,
} from '@/data';

/**
 * Hook for accessing all services
 * @returns Array of all services
 */
export const useServices = (): Service[] => {
    return services;
};

/**
 * Hook for getting featured services
 * @returns Array of featured services
 */
export const useFeaturedServices = (): Service[] => {
    return getFeaturedServices();
};

/**
 * Hook for getting service by ID
 * @param id - Service ID
 * @returns Service or undefined
 */
export const useServiceById = (id: string): Service | undefined => {
    return getServiceById(id);
};

/**
 * Hook for filtering services by category
 * @param category - Service category
 * @returns Array of services in category
 */
export const useServicesByCategory = (category: string): Service[] => {
    return getServicesByCategory(category);
};

/**
 * Hook for filtering services by technology
 * @param technology - Technology name
 * @returns Array of services using technology
 */
export const useServicesByTechnology = (technology: string): Service[] => {
    return getServicesByTechnology(technology);
};

/**
 * Hook for getting all service categories
 * @returns Array of unique categories
 */
export const useServiceCategories = (): string[] => {
    const categories = new Set<string>();
    services.forEach((s) => categories.add(s.category));
    return Array.from(categories);
};

/**
 * Hook for getting all technologies across services
 * @returns Array of unique technologies
 */
export const useServiceTechnologies = (): string[] => {
    const technologies = new Set<string>();
    services.forEach((s) => {
        s.technologies.forEach((tech) => technologies.add(tech));
    });
    return Array.from(technologies);
};

/**
 * Hook for getting featured service count
 * @returns Number of featured services
 */
export const useFeaturedServiceCount = (): number => {
    return getFeaturedServices().length;
};

/**
 * Hook for getting total service count
 * @returns Total number of services
 */
export const useServiceCount = (): number => {
    return services.length;
};
