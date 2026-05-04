import { useMemo, useState } from 'react';

interface SearchOptions {
    fields: string[];
    caseSensitive?: boolean;
    fuzzy?: boolean;
}

/**
 * Hook for searching items in an array
 * @param items - Array of items to search
 * @param options - Search configuration
 * @returns Search state and results
 */
export const useSearch = <T extends Record<string, any>>(
    items: T[],
    options: SearchOptions,
) => {
    const [query, setQuery] = useState('');

    const results = useMemo(() => {
        if (!query.trim()) return items;

        const lowerQuery = options.caseSensitive ? query : query.toLowerCase();

        return items.filter((item) => {
            return options.fields.some((field) => {
                const value = String(item[field] || '');
                const searchValue = options.caseSensitive ? value : value.toLowerCase();

                if (options.fuzzy) {
                    return fuzzyMatch(lowerQuery, searchValue);
                }
                return searchValue.includes(lowerQuery);
            });
        });
    }, [query, items, options]);

    return {
        query,
        setQuery,
        results,
        resultCount: results.length,
        isEmpty: results.length === 0,
        hasResults: results.length > 0,
    };
};

/**
 * Fuzzy matching algorithm
 * @param query - Search query
 * @param text - Text to match against
 * @returns True if fuzzy match succeeds
 */
const fuzzyMatch = (query: string, text: string): boolean => {
    let queryIndex = 0;

    for (let i = 0; i < text.length; i++) {
        if (query[queryIndex] === text[i]) {
            queryIndex++;
        }
    }

    return queryIndex === query.length;
};

/**
 * Hook for filtering items by multiple criteria
 * @param items - Array of items to filter
 * @returns Filter state and results
 */
export const useFilter = <T extends Record<string, any>>(items: T[]) => {
    const [filters, setFilters] = useState<Record<string, any>>({});

    const results = useMemo(() => {
        return items.filter((item) => {
            return Object.entries(filters).every(([key, value]) => {
                if (value === null || value === undefined) return true;

                if (Array.isArray(value)) {
                    return value.includes(item[key]);
                }

                if (typeof value === 'function') {
                    return value(item[key]);
                }

                return item[key] === value;
            });
        });
    }, [items, filters]);

    const addFilter = (key: string, value: any) => {
        setFilters((prev) => ({
            ...prev,
            [key]: value,
        }));
    };

    const removeFilter = (key: string) => {
        setFilters((prev) => {
            const newFilters = { ...prev };
            delete newFilters[key];
            return newFilters;
        });
    };

    const clearFilters = () => {
        setFilters({});
    };

    return {
        filters,
        results,
        resultCount: results.length,
        addFilter,
        removeFilter,
        clearFilters,
    };
};

/**
 * Hook for combined search and filter
 * @param items - Array of items
 * @param searchFields - Fields to search in
 * @returns Search and filter functionality
 */
export const useSearchAndFilter = <T extends Record<string, any>>(
    items: T[],
    searchFields: string[],
) => {
    const search = useSearch(items, { fields: searchFields });
    const filter = useFilter(search.results);

    return {
        ...search,
        ...filter,
        results: filter.results,
        resultCount: filter.results.length,
    };
};
