import { useState } from 'react';

interface PaginationState {
    currentPage: number;
    pageSize: number;
    totalItems: number;
    totalPages: number;
}

interface PaginationControls {
    state: PaginationState;
    goToPage: (page: number) => void;
    nextPage: () => void;
    previousPage: () => void;
    setPageSize: (size: number) => void;
}

/**
 * Hook for paginating data
 * @param items - Array of items to paginate
 * @param initialPageSize - Initial page size (default: 10)
 * @returns Pagination state and controls
 */
export const usePagination = <T,>(items: T[], initialPageSize: number = 10): PaginationControls & { items: T[] } => {
    const [currentPage, setCurrentPage] = useState(1);
    const [pageSize, setPageSize] = useState(initialPageSize);

    const totalItems = items.length;
    const totalPages = Math.ceil(totalItems / pageSize);

    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    const paginatedItems = items.slice(startIndex, endIndex);

    const goToPage = (page: number) => {
        const validPage = Math.max(1, Math.min(page, totalPages));
        setCurrentPage(validPage);
    };

    const nextPage = () => goToPage(currentPage + 1);
    const previousPage = () => goToPage(currentPage - 1);

    const handleSetPageSize = (size: number) => {
        setPageSize(Math.max(1, size));
        setCurrentPage(1);
    };

    return {
        items: paginatedItems,
        state: {
            currentPage,
            pageSize,
            totalItems,
            totalPages,
        },
        goToPage,
        nextPage,
        previousPage,
        setPageSize: handleSetPageSize,
    };
};

/**
 * Hook for getting page range info
 * @param currentPage - Current page number
 * @param pageSize - Page size
 * @returns Object with start and end item numbers
 */
export const usePageInfo = (currentPage: number, pageSize: number) => {
    const startItem = (currentPage - 1) * pageSize + 1;
    const endItem = currentPage * pageSize;

    return { startItem, endItem };
};

/**
 * Hook for checking pagination state
 * @param state - Pagination state
 * @returns Object with boolean flags
 */
export const usePaginationFlags = (state: PaginationState) => {
    return {
        isFirstPage: state.currentPage === 1,
        isLastPage: state.currentPage === state.totalPages,
        canGoPrevious: state.currentPage > 1,
        canGoNext: state.currentPage < state.totalPages,
    };
};
