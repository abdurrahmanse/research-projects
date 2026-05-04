import type { FAQ } from '../types/types';

/**
 * FAQs
 * Contains frequently asked questions
 * Used on: FAQ Page, Help Section
 */

export const faqs: FAQ[] = [
    {
        id: 'faq-001',
        question: 'What services do you offer?',
        answer:
            'I offer a comprehensive range of services including machine learning solutions, data engineering, full-stack web development, performance optimization, NLP and text analysis, and AI/ML consulting. Each service is customized to your specific needs and business objectives.',
        category: 'Services',
        priority: 1,
    },
    {
        id: 'faq-002',
        question: 'What is your typical project timeline?',
        answer:
            'Project timelines vary depending on complexity and scope. Typically, optimization projects take 2-6 weeks, while full-stack development can take 8-20 weeks, and ML solutions 4-12 weeks. I always provide a detailed timeline estimate after understanding your requirements.',
        category: 'Projects',
        priority: 2,
    },
    {
        id: 'faq-003',
        question: 'Do you work remotely?',
        answer:
            'Yes, I work exclusively remotely and have successfully completed projects with clients across different continents. I use modern communication tools and maintain clear documentation to ensure smooth collaboration.',
        category: 'Work',
        priority: 3,
    },
    {
        id: 'faq-004',
        question: 'How do you approach new projects?',
        answer:
            'I start with a thorough discovery phase to understand your business goals, technical requirements, and constraints. Then I develop a detailed proposal with timeline, deliverables, and cost. Throughout the project, I maintain regular communication and provide progress updates.',
        category: 'Process',
        priority: 1,
    },
    {
        id: 'faq-005',
        question: 'Can you help with existing projects?',
        answer:
            'Absolutely. I offer services for debugging existing code, performance optimization, feature additions, and architecture improvements. If you have a project that needs help, let\'s discuss your specific challenges.',
        category: 'Services',
        priority: 2,
    },
    {
        id: 'faq-006',
        question: 'What technologies do you specialize in?',
        answer:
            'My expertise spans across multiple domains: Frontend (React, Next.js, TypeScript), Backend (Node.js, Python), Data Science (Machine Learning, Deep Learning, NLP), Cloud (AWS, Google Cloud), and DevOps (Docker, Kubernetes). I\'m always learning new technologies relevant to client needs.',
        category: 'Technology',
        priority: 1,
    },
];

/**
 * Get FAQ by ID
 */
export const getFAQById = (id: string): FAQ | undefined => {
    return faqs.find((faq) => faq.id === id);
};

/**
 * Get FAQs by category
 */
export const getFAQByCategory = (category: string): FAQ[] => {
    return faqs.filter((faq) => faq.category === category);
};

/**
 * Get FAQs sorted by priority
 */
export const getFAQsSortedByPriority = (): FAQ[] => {
    return [...faqs].sort((a, b) => a.priority - b.priority);
};

/**
 * Get all unique categories
 */
export const getCategories = (): string[] => {
    const categories = new Set<string>();
    faqs.forEach((faq) => {
        categories.add(faq.category);
    });
    return Array.from(categories);
};

/**
 * Search FAQs
 */
export const searchFAQs = (query: string): FAQ[] => {
    const lowerQuery = query.toLowerCase();
    return faqs.filter(
        (faq) =>
            faq.question.toLowerCase().includes(lowerQuery) || faq.answer.toLowerCase().includes(lowerQuery),
    );
};

export default faqs;
