import type { Testimonial } from '@/data';
import {
    getAverageRating,
    getRelationships,
    getTestimonialById,
    getTestimonialCompanies,
    getTestimonialCountByRating,
    getTestimonialsByCompany,
    getTestimonialsByRating,
    getTestimonialsByRelationship,
    getVerifiedTestimonials,
    testimonials,
} from '@/data';

/**
 * Hook for accessing all testimonials
 * @returns Array of all testimonials
 */
export const useTestimonials = (): Testimonial[] => {
    return testimonials;
};

/**
 * Hook for getting testimonial by ID
 * @param id - Testimonial ID
 * @returns Testimonial or undefined
 */
export const useTestimonialById = (id: string): Testimonial | undefined => {
    return getTestimonialById(id);
};

/**
 * Hook for filtering testimonials by rating
 * @param rating - Star rating (1-5)
 * @returns Array of testimonials with rating
 */
export const useTestimonialsByRating = (rating: number): Testimonial[] => {
    return getTestimonialsByRating(rating);
};

/**
 * Hook for filtering testimonials by relationship
 * @param relationship - Relationship type
 * @returns Array of testimonials from relationship
 */
export const useTestimonialsByRelationship = (relationship: string): Testimonial[] => {
    return getTestimonialsByRelationship(relationship);
};

/**
 * Hook for getting verified testimonials only
 * @returns Array of verified testimonials
 */
export const useVerifiedTestimonials = (): Testimonial[] => {
    return getVerifiedTestimonials();
};

/**
 * Hook for filtering testimonials by company
 * @param company - Company name
 * @returns Array of testimonials from company
 */
export const useTestimonialsByCompany = (company: string): Testimonial[] => {
    return getTestimonialsByCompany(company);
};

/**
 * Hook for getting all companies mentioned in testimonials
 * @returns Array of company names
 */
export const useTestimonialCompanies = (): string[] => {
    return getTestimonialCompanies();
};

/**
 * Hook for getting all relationship types
 * @returns Array of relationship types
 */
export const useTestimonialRelationships = (): string[] => {
    return getRelationships();
};

/**
 * Hook for getting average testimonial rating
 * @returns Average rating (0-5)
 */
export const useAverageTestimonialRating = (): number => {
    return getAverageRating();
};

/**
 * Hook for getting testimonial count by rating
 * @returns Object with rating as key and count as value
 */
export const useTestimonialCountByRating = (): Record<number, number> => {
    return getTestimonialCountByRating();
};

/**
 * Hook for getting verified testimonial count
 * @returns Number of verified testimonials
 */
export const useVerifiedTestimonialCount = (): number => {
    return getVerifiedTestimonials().length;
};

/**
 * Hook for getting total testimonial count
 * @returns Total number of testimonials
 */
export const useTestimonialCount = (): number => {
    return testimonials.length;
};

/**
 * Hook for checking if all testimonials are 5-star
 * @returns True if all testimonials are 5-star
 */
export const useAllFiveStarTestimonials = (): boolean => {
    return testimonials.every((t) => t.rating === 5);
};
