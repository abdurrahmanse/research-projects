import type { BlogPost } from '../types/types';

/**
 * Blog Posts
 * Contains all published blog articles
 * Used on: Blog Page, Homepage (featured)
 */

export const blogPosts: BlogPost[] = [
    {
        id: 'blog-001',
        title: 'Understanding Transformer Models: From Theory to Implementation',
        slug: 'understanding-transformers',
        excerpt:
            'A deep dive into how transformer models work, why they\'re revolutionary, and a step-by-step guide to implementing one from scratch.',
        content:
            'Transformer models have revolutionized the field of NLP and beyond. In this comprehensive guide, we\'ll explore the architecture, understand the mathematics behind attention mechanisms, and implement a transformer from scratch using PyTorch...',
        author: 'Abdur Rahman',
        publishedDate: '2024-08-20',
        updatedDate: '2024-09-10',
        category: 'Machine Learning',
        tags: ['Transformers', 'NLP', 'Deep Learning', 'PyTorch'],
        readTime: 15,
        image: '/assets/blog/transformers.jpg',
        featured: true,
        views: 3456,
        likes: 234,
        comments: 45,
    },
    {
        id: 'blog-002',
        title: 'Building Production-Ready ML Systems: Lessons from Real Projects',
        slug: 'production-ml-systems',
        excerpt:
            'Insights from deploying multiple ML projects to production, covering data pipeline design, model monitoring, and scaling challenges.',
        content:
            'Building ML projects for academic purposes is one thing, but deploying them to production environments where millions of users depend on them is entirely different. In this article, I\'ll share lessons learned from shipping multiple ML systems to production...',
        author: 'Abdur Rahman',
        publishedDate: '2024-07-15',
        category: 'MLOps',
        tags: ['ML', 'Production', 'DevOps', 'Monitoring'],
        readTime: 12,
        image: '/assets/blog/production-ml.jpg',
        featured: true,
        views: 2891,
        likes: 189,
        comments: 32,
    },
    {
        id: 'blog-003',
        title: 'React Performance Optimization: Advanced Techniques',
        slug: 'react-performance',
        excerpt:
            'Advanced techniques for optimizing React applications including code splitting, lazy loading, and component memoization.',
        content:
            'React is powerful, but poorly optimized React applications can become sluggish. This guide covers advanced optimization techniques that helped me achieve a 50% performance improvement on a major e-commerce platform...',
        author: 'Abdur Rahman',
        publishedDate: '2024-06-10',
        updatedDate: '2024-07-05',
        category: 'Frontend',
        tags: ['React', 'Performance', 'Optimization', 'JavaScript'],
        readTime: 10,
        image: '/assets/blog/react-performance.jpg',
        featured: false,
        views: 4123,
        likes: 312,
        comments: 58,
    },
    {
        id: 'blog-004',
        title: 'Data Pipeline Architecture: Designing Scalable Systems',
        slug: 'data-pipeline-architecture',
        excerpt: 'Best practices for designing data pipelines that can handle millions of events, ensuring reliability and performance.',
        content:
            'Designing data pipelines is crucial for any data-driven organization. We\'ll explore architectural patterns, technology choices, and best practices for building reliable, scalable data pipelines...',
        author: 'Abdur Rahman',
        publishedDate: '2024-05-22',
        category: 'Data Engineering',
        tags: ['Data Engineering', 'Architecture', 'Scalability', 'Apache Spark'],
        readTime: 14,
        image: '/assets/blog/data-pipeline.jpg',
        featured: true,
        views: 2345,
        likes: 156,
        comments: 28,
    },
    {
        id: 'blog-005',
        title: 'Customer Segmentation with Machine Learning: A Practical Guide',
        slug: 'customer-segmentation-ml',
        excerpt: 'Step-by-step guide to building ML models for customer segmentation with real-world examples and code.',
        content:
            'Customer segmentation is one of the most valuable applications of machine learning in business. Learn how to prepare data, select algorithms, and deploy segmentation models in production...',
        author: 'Abdur Rahman',
        publishedDate: '2024-04-18',
        category: 'Machine Learning',
        tags: ['ML', 'Business Analytics', 'Segmentation', 'Python'],
        readTime: 11,
        image: '/assets/blog/segmentation-ml.jpg',
        featured: false,
        views: 1876,
        likes: 123,
        comments: 19,
    },
    {
        id: 'blog-006',
        title: 'NLP for Healthcare: Building AI Solutions for Medical Applications',
        slug: 'nlp-healthcare',
        excerpt:
            'Exploring NLP techniques specifically designed for healthcare applications and the unique challenges they present.',
        content:
            'Healthcare is one of the most important sectors where AI can make a real difference. In this article, we\'ll explore how NLP can be applied to healthcare challenges, from patient communication to medical coding...',
        author: 'Abdur Rahman',
        publishedDate: '2024-03-25',
        updatedDate: '2024-04-05',
        category: 'NLP',
        tags: ['NLP', 'Healthcare', 'AI', 'Deep Learning'],
        readTime: 13,
        image: '/assets/blog/nlp-healthcare.jpg',
        featured: true,
        views: 3234,
        likes: 267,
        comments: 41,
    },
];

/**
 * Get blog post by ID
 */
export const getBlogPostById = (id: string): BlogPost | undefined => {
    return blogPosts.find((post) => post.id === id);
};

/**
 * Get blog post by slug
 */
export const getBlogPostBySlug = (slug: string): BlogPost | undefined => {
    return blogPosts.find((post) => post.slug === slug);
};

/**
 * Get featured blog posts
 */
export const getFeaturedBlogPosts = (): BlogPost[] => {
    return blogPosts.filter((post) => post.featured).slice(0, 3);
};

/**
 * Get blog posts by category
 */
export const getBlogPostsByCategory = (category: string): BlogPost[] => {
    return blogPosts.filter((post) => post.category === category);
};

/**
 * Get blog posts by tag
 */
export const getBlogPostsByTag = (tag: string): BlogPost[] => {
    return blogPosts.filter((post) => post.tags.includes(tag));
};

/**
 * Get blog posts sorted by date (newest first)
 */
export const getBlogPostsSortedByDate = (): BlogPost[] => {
    return [...blogPosts].sort((a, b) => new Date(b.publishedDate).getTime() - new Date(a.publishedDate).getTime());
};

/**
 * Get blog posts sorted by views (most viewed first)
 */
export const getBlogPostsSortedByViews = (): BlogPost[] => {
    return [...blogPosts].sort((a, b) => b.views - a.views);
};

/**
 * Get all blog categories
 */
export const getCategories = (): string[] => {
    const categories = new Set<string>();
    blogPosts.forEach((post) => {
        categories.add(post.category);
    });
    return Array.from(categories);
};

/**
 * Get all blog tags
 */
export const getAllTags = (): string[] => {
    const tags = new Set<string>();
    blogPosts.forEach((post) => {
        post.tags.forEach((tag) => {
            tags.add(tag);
        });
    });
    return Array.from(tags);
};

/**
 * Get total blog views
 */
export const getTotalBlogViews = (): number => {
    return blogPosts.reduce((total, post) => total + post.views, 0);
};

/**
 * Get most viewed blog post
 */
export const getMostViewedBlogPost = (): BlogPost | undefined => {
    return blogPosts.reduce((prev, current) => (prev.views > current.views ? prev : current));
};

/**
 * Search blog posts
 */
export const searchBlogPosts = (query: string): BlogPost[] => {
    const lowerQuery = query.toLowerCase();
    return blogPosts.filter(
        (post) =>
            post.title.toLowerCase().includes(lowerQuery) ||
            post.excerpt.toLowerCase().includes(lowerQuery) ||
            post.tags.some((tag) => tag.toLowerCase().includes(lowerQuery)),
    );
};

export default blogPosts;
