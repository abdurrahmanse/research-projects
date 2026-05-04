import type { CaseStudy } from '@/data';
import {
    caseStudies,
    getCaseStudiesByCompany,
    getCaseStudiesByIndustry,
    getCaseStudyById,
    getCaseStudyBySlug,
    getCaseStudyCompanies,
    getCaseStudyIndustries,
} from '@/data';

/**
 * Hook for accessing all case studies
 * @returns Array of all case studies
 */
export const useCaseStudies = (): CaseStudy[] => {
    return caseStudies;
};

/**
 * Hook for getting case study by ID
 * @param id - Case study ID
 * @returns Case study or undefined
 */
export const useCaseStudyById = (id: string): CaseStudy | undefined => {
    return getCaseStudyById(id);
};

/**
 * Hook for getting case study by slug
 * @param slug - URL slug
 * @returns Case study or undefined
 */
export const useCaseStudyBySlug = (slug: string): CaseStudy | undefined => {
    return getCaseStudyBySlug(slug);
};

/**
 * Hook for filtering case studies by industry
 * @param industry - Industry name
 * @returns Array of case studies in industry
 */
export const useCaseStudiesByIndustry = (industry: string): CaseStudy[] => {
    return getCaseStudiesByIndustry(industry);
};

/**
 * Hook for filtering case studies by company
 * @param company - Company name
 * @returns Array of case studies for company
 */
export const useCaseStudiesByCompany = (company: string): CaseStudy[] => {
    return getCaseStudiesByCompany(company);
};

/**
 * Hook for getting all industries
 * @returns Array of unique industry names
 */
export const useCaseStudyIndustries = (): string[] => {
    return getCaseStudyIndustries();
};

/**
 * Hook for getting all companies
 * @returns Array of company names
 */
export const useCaseStudyCompanies = (): string[] => {
    return getCaseStudyCompanies();
};

/**
 * Hook for getting case study count
 * @returns Total number of case studies
 */
export const useCaseStudyCount = (): number => {
    return caseStudies.length;
};
