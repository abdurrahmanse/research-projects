import type { BlogPost } from '@/data';
import {
    blogPosts,
    getBlogPostById,
    getBlogPostBySlug,
    getBlogPostsByCategory,
    getBlogPostsByTag,
    getBlogPostsSortedByDate,
    getBlogPostsSortedByViews,
    getFeaturedBlogPosts,
    getMostViewedBlogPost,
    getTotalBlogViews,
    searchBlogPosts,
} from '@/data';

/**
 * Hook for accessing all blog posts
 * @returns Array of all blog posts
 */
export const useBlogPosts = (): BlogPost[] => {
    return blogPosts;
};

/**
 * Hook for getting featured blog posts
 * @returns Array of featured blog posts
 */
export const useFeaturedBlogPosts = (): BlogPost[] => {
    return getFeaturedBlogPosts();
};

/**
 * Hook for getting blog post by ID
 * @param id - Blog post ID
 * @returns Blog post or undefined
 */
export const useBlogPostById = (id: string): BlogPost | undefined => {
    return getBlogPostById(id);
};

/**
 * Hook for getting blog post by slug
 * @param slug - URL slug
 * @returns Blog post or undefined
 */
export const useBlogPostBySlug = (slug: string): BlogPost | undefined => {
    return getBlogPostBySlug(slug);
};

/**
 * Hook for filtering blog posts by category
 * @param category - Blog category
 * @returns Array of blog posts in category
 */
export const useBlogPostsByCategory = (category: string): BlogPost[] => {
    return getBlogPostsByCategory(category);
};

/**
 * Hook for filtering blog posts by tag
 * @param tag - Blog tag
 * @returns Array of blog posts with tag
 */
export const useBlogPostsByTag = (tag: string): BlogPost[] => {
    return getBlogPostsByTag(tag);
};

/**
 * Hook for getting blog posts sorted by date (newest first)
 * @returns Array of blog posts sorted by date
 */
export const useBlogPostsSortedByDate = (): BlogPost[] => {
    return getBlogPostsSortedByDate();
};

/**
 * Hook for getting blog posts sorted by views (most viewed first)
 * @returns Array of blog posts sorted by views
 */
export const useBlogPostsSortedByViews = (): BlogPost[] => {
    return getBlogPostsSortedByViews();
};

/**
 * Hook for getting total blog views
 * @returns Total view count
 */
export const useTotalBlogViews = (): number => {
    return getTotalBlogViews();
};

/**
 * Hook for getting most viewed blog post
 * @returns Most viewed blog post or undefined
 */
export const useMostViewedBlogPost = (): BlogPost | undefined => {
    return getMostViewedBlogPost();
};

/**
 * Hook for searching blog posts
 * @param query - Search query
 * @returns Array of matching blog posts
 */
export const useSearchBlogPosts = (query: string): BlogPost[] => {
    return searchBlogPosts(query);
};

/**
 * Hook for getting all blog categories
 * @returns Array of unique categories
 */
export const useBlogCategories = (): string[] => {
    const categories = new Set<string>();
    blogPosts.forEach((post) => categories.add(post.category));
    return Array.from(categories);
};

/**
 * Hook for getting all blog tags
 * @returns Array of unique tags
 */
export const useBlogTags = (): string[] => {
    const tags = new Set<string>();
    blogPosts.forEach((post) => {
        post.tags.forEach((tag) => tags.add(tag));
    });
    return Array.from(tags);
};

/**
 * Hook for getting blog post count
 * @returns Total number of blog posts
 */
export const useBlogPostCount = (): number => {
    return blogPosts.length;
};

/**
 * Hook for getting average read time
 * @returns Average read time in minutes
 */
export const useAverageBlogReadTime = (): number => {
    return blogPosts.length > 0 ? Math.round(blogPosts.reduce((sum, post) => sum + post.readTime, 0) / blogPosts.length) : 0;
};
