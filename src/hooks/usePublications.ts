import type { Publication } from '@/data';
import {
    getAllKeywords,
    getMostCitedPublication,
    getMostDownloadedPublication,
    getPublicationById,
    getPublicationsByAuthor,
    getPublicationsByResearchArea,
    getResearchAreas,
    getTotalCitations,
    getTotalDownloads,
    publications,
} from '@/data';

/**
 * Hook for accessing all publications
 * @returns Array of all publications
 */
export const usePublications = (): Publication[] => {
    return publications;
};

/**
 * Hook for getting publication by ID
 * @param id - Publication ID
 * @returns Publication or undefined
 */
export const usePublicationById = (id: string): Publication | undefined => {
    return getPublicationById(id);
};

/**
 * Hook for getting publications by author
 * @param author - Author name
 * @returns Array of publications by author
 */
export const usePublicationsByAuthor = (author: string): Publication[] => {
    return getPublicationsByAuthor(author);
};

/**
 * Hook for getting publications by research area
 * @param area - Research area name
 * @returns Array of publications in area
 */
export const usePublicationsByResearchArea = (area: string): Publication[] => {
    return getPublicationsByResearchArea(area);
};

/**
 * Hook for getting total citations
 * @returns Total citation count
 */
export const useTotalCitations = (): number => {
    return getTotalCitations();
};

/**
 * Hook for getting total downloads
 * @returns Total download count
 */
export const useTotalDownloads = (): number => {
    return getTotalDownloads();
};

/**
 * Hook for getting most cited publication
 * @returns Most cited publication or undefined
 */
export const useMostCitedPublication = (): Publication | undefined => {
    return getMostCitedPublication();
};

/**
 * Hook for getting most downloaded publication
 * @returns Most downloaded publication or undefined
 */
export const useMostDownloadedPublication = (): Publication | undefined => {
    return getMostDownloadedPublication();
};

/**
 * Hook for getting all research areas
 * @returns Array of research area names
 */
export const useResearchAreas = (): string[] => {
    return getResearchAreas();
};

/**
 * Hook for getting all publication keywords
 * @returns Array of unique keywords
 */
export const usePublicationKeywords = (): string[] => {
    return getAllKeywords();
};

/**
 * Hook for getting publication count
 * @returns Total number of publications
 */
export const usePublicationCount = (): number => {
    return publications.length;
};

/**
 * Hook for getting average citations per publication
 * @returns Average citation count
 */
export const useAverageCitationsPerPublication = (): number => {
    return publications.length > 0 ? getTotalCitations() / publications.length : 0;
};
