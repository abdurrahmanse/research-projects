import { useMemo, useState } from 'react';

type SortOrder = 'asc' | 'desc';

interface SortState {
    field: string | null;
    order: SortOrder;
}

/**
 * Hook for sorting items in an array
 * @param items - Array of items to sort
 * @param initialField - Initial sort field
 * @param initialOrder - Initial sort order
 * @returns Sort state and results
 */
export const useSort = <T extends Record<string, any>>(
    items: T[],
    initialField: string | null = null,
    initialOrder: SortOrder = 'asc',
) => {
    const [sortState, setSortState] = useState<SortState>({
        field: initialField,
        order: initialOrder,
    });

    const results = useMemo(() => {
        if (!sortState.field) return items;

        const sorted = [...items].sort((a, b) => {
            const aValue = a[sortState.field!];
            const bValue = b[sortState.field!];

            if (aValue === bValue) return 0;

            let comparison = 0;
            if (typeof aValue === 'string' && typeof bValue === 'string') {
                comparison = aValue.localeCompare(bValue);
            } else if (typeof aValue === 'number' && typeof bValue === 'number') {
                comparison = aValue - bValue;
            } else if (aValue instanceof Date && bValue instanceof Date) {
                comparison = aValue.getTime() - bValue.getTime();
            } else {
                comparison = String(aValue).localeCompare(String(bValue));
            }

            return sortState.order === 'asc' ? comparison : -comparison;
        });

        return sorted;
    }, [items, sortState]);

    const setSortField = (field: string) => {
        setSortState((prev) => ({
            field,
            order: prev.field === field && prev.order === 'asc' ? 'desc' : 'asc',
        }));
    };

    const setSortOrder = (order: SortOrder) => {
        setSortState((prev) => ({
            ...prev,
            order,
        }));
    };

    const clearSort = () => {
        setSortState({
            field: null,
            order: 'asc',
        });
    };

    return {
        results,
        sortField: sortState.field,
        sortOrder: sortState.order,
        setSortField,
        setSortOrder,
        clearSort,
        isSorted: sortState.field !== null,
    };
};

/**
 * Hook for sorting with custom comparator
 * @param items - Array of items
 * @param comparator - Custom comparison function
 * @returns Sorted items and sort controls
 */
export const useSortCustom = <T,>(
    items: T[],
    comparator: (a: T, b: T) => number,
) => {
    const [order, setOrder] = useState<SortOrder>('asc');

    const results = useMemo(() => {
        const sorted = [...items].sort(comparator);
        return order === 'asc' ? sorted : sorted.reverse();
    }, [items, comparator, order]);

    const toggleOrder = () => {
        setOrder((prev) => (prev === 'asc' ? 'desc' : 'asc'));
    };

    return {
        results,
        order,
        toggleOrder,
    };
};

/**
 * Hook for multi-field sorting
 * @param items - Array of items
 * @param sortFields - Array of fields to sort by (in priority order)
 * @returns Sort state and results
 */
export const useMultiSort = <T extends Record<string, any>>(
    items: T[],
    sortFields: Array<{ field: string; order: SortOrder }> = [],
) => {
    const [sorts, setSorts] = useState(sortFields);

    const results = useMemo(() => {
        if (sorts.length === 0) return items;

        return [...items].sort((a, b) => {
            for (const sort of sorts) {
                const aValue = a[sort.field];
                const bValue = b[sort.field];

                if (aValue === bValue) continue;

                let comparison = 0;
                if (typeof aValue === 'string' && typeof bValue === 'string') {
                    comparison = aValue.localeCompare(bValue);
                } else if (typeof aValue === 'number' && typeof bValue === 'number') {
                    comparison = aValue - bValue;
                } else {
                    comparison = String(aValue).localeCompare(String(bValue));
                }

                return sort.order === 'asc' ? comparison : -comparison;
            }
            return 0;
        });
    }, [items, sorts]);

    const addSort = (field: string, order: SortOrder = 'asc') => {
        setSorts((prev) => [...prev, { field, order }]);
    };

    const removeSort = (field: string) => {
        setSorts((prev) => prev.filter((s) => s.field !== field));
    };

    const clearSorts = () => {
        setSorts([]);
    };

    return {
        results,
        sorts,
        addSort,
        removeSort,
        clearSorts,
    };
};
