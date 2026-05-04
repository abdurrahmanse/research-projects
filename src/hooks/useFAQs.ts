import type { FAQ } from '@/data';
import {
    faqs,
    getFAQByCategory,
    getFAQById,
    getFAQCategories,
    getFAQsSortedByPriority,
    searchFAQs,
} from '@/data';

/**
 * Hook for accessing all FAQs
 * @returns Array of all FAQs
 */
export const useFAQs = (): FAQ[] => {
    return faqs;
};

/**
 * Hook for getting FAQ by ID
 * @param id - FAQ ID
 * @returns FAQ or undefined
 */
export const useFAQById = (id: string): FAQ | undefined => {
    return getFAQById(id);
};

/**
 * Hook for filtering FAQs by category
 * @param category - FAQ category
 * @returns Array of FAQs in category
 */
export const useFAQsByCategory = (category: string): FAQ[] => {
    return getFAQByCategory(category);
};

/**
 * Hook for getting FAQs sorted by priority
 * @returns Array of FAQs sorted by priority (ascending)
 */
export const useFAQsSortedByPriority = (): FAQ[] => {
    return getFAQsSortedByPriority();
};

/**
 * Hook for getting all FAQ categories
 * @returns Array of unique categories
 */
export const useFAQCategories = (): string[] => {
    return getFAQCategories();
};

/**
 * Hook for searching FAQs
 * @param query - Search query
 * @returns Array of matching FAQs
 */
export const useSearchFAQs = (query: string): FAQ[] => {
    return searchFAQs(query);
};

/**
 * Hook for getting FAQ count by category
 * @returns Object with category as key and count as value
 */
export const useFAQCountByCategory = (): Record<string, number> => {
    const counts: Record<string, number> = {};
    faqs.forEach((faq) => {
        counts[faq.category] = (counts[faq.category] || 0) + 1;
    });
    return counts;
};

/**
 * Hook for getting total FAQ count
 * @returns Total number of FAQs
 */
export const useFAQCount = (): number => {
    return faqs.length;
};

/**
 * Hook for getting most common FAQ category
 * @returns Most common category name or undefined
 */
export const useMostCommonFAQCategory = (): string | undefined => {
    const counts = useFAQCountByCategory();
    return Object.keys(counts).reduce((max, current) =>
        counts[current] > counts[max] ? current : max
    );
};
