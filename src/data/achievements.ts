import type { Achievement } from '../types/types';

/**
 * Achievements
 * Contains all awards, recognitions, and accolades
 * Used on: Achievements Page, About Page
 */

export const achievements: Achievement[] = [
    {
        id: 'achievement-001',
        title: 'Innovation Excellence Award',
        category: 'Technology Innovation',
        issuer: 'Tech Leaders Global',
        awardDate: '2024-06-15',
        description:
            'Recognized for developing innovative healthcare AI solutions that transformed patient care delivery.',
        impact: 'Received for creating the Healthcare AI Chatbot that improved patient satisfaction by 45%.',
        badge: '/assets/badges/innovation-excellence.png',
        featured: true,
    },
    {
        id: 'achievement-002',
        title: 'Machine Learning Excellence',
        category: 'AI & Machine Learning',
        issuer: 'Data Science Summit',
        awardDate: '2024-04-22',
        description: 'Awarded for outstanding contributions to machine learning and data science.',
        impact:
            'Recognition for developing advanced customer segmentation models that achieved 87% accuracy improvement.',
        badge: '/assets/badges/ml-excellence.png',
        featured: true,
    },
    {
        id: 'achievement-003',
        title: 'Performance Optimization Champion',
        category: 'Software Performance',
        issuer: 'Web Development Summit',
        awardDate: '2024-02-28',
        description: 'Recognized for exceptional web performance optimization achieving 50% improvement.',
        impact: 'Awarded for e-commerce platform optimization project resulting in 28% conversion rate increase.',
        badge: '/assets/badges/performance-champion.png',
        featured: true,
    },
    {
        id: 'achievement-004',
        title: 'Top Data Science Contributor',
        category: 'Research & Publication',
        issuer: 'International Journal of AI',
        awardDate: '2023-11-10',
        description: 'Recognition for high-impact research publications in AI and machine learning.',
        impact: 'Received for 4 published papers with 82+ total citations in prestigious journals.',
        badge: '/assets/badges/research-contributor.png',
        featured: false,
    },
    {
        id: 'achievement-005',
        title: 'Community Impact Award',
        category: 'Community & Education',
        issuer: 'Tech Community Leaders',
        awardDate: '2023-09-05',
        description: 'Awarded for mentoring junior developers and contributing to open-source projects.',
        impact: 'Recognized for creating educational content and mentoring over 50 junior developers.',
        badge: '/assets/badges/community-impact.png',
        featured: false,
    },
    {
        id: 'achievement-006',
        title: 'Enterprise Solutions Leader',
        category: 'Enterprise Technology',
        issuer: 'Enterprise Tech Council',
        awardDate: '2023-07-18',
        description: 'Recognition for developing scalable enterprise solutions.',
        impact: 'Awarded for building ML and AI solutions deployed across multiple Fortune 500 companies.',
        badge: '/assets/badges/enterprise-leader.png',
        featured: false,
    },
];

/**
 * Get achievement by ID
 */
export const getAchievementById = (id: string): Achievement | undefined => {
    return achievements.find((achievement) => achievement.id === id);
};

/**
 * Get featured achievements
 */
export const getFeaturedAchievements = (): Achievement[] => {
    return achievements.filter((achievement) => achievement.featured);
};

/**
 * Get achievements by category
 */
export const getAchievementsByCategory = (category: string): Achievement[] => {
    return achievements.filter((achievement) => achievement.category === category);
};

/**
 * Get achievements by issuer
 */
export const getAchievementsByIssuer = (issuer: string): Achievement[] => {
    return achievements.filter((achievement) => achievement.issuer === issuer);
};

/**
 * Get achievements sorted by date (newest first)
 */
export const getAchievementsSortedByDate = (): Achievement[] => {
    return [...achievements].sort((a, b) => new Date(b.awardDate).getTime() - new Date(a.awardDate).getTime());
};

/**
 * Get all achievement categories
 */
export const getCategories = (): string[] => {
    const categories = new Set<string>();
    achievements.forEach((achievement) => {
        categories.add(achievement.category);
    });
    return Array.from(categories);
};

/**
 * Get all achievement issuers
 */
export const getIssuers = (): string[] => {
    const issuers = new Set<string>();
    achievements.forEach((achievement) => {
        issuers.add(achievement.issuer);
    });
    return Array.from(issuers);
};

/**
 * Get achievement count by year
 */
export const getAchievementCountByYear = (): Record<string, number> => {
    const yearCounts: Record<string, number> = {};
    achievements.forEach((achievement) => {
        const year = new Date(achievement.awardDate).getFullYear().toString();
        yearCounts[year] = (yearCounts[year] || 0) + 1;
    });
    return yearCounts;
};

export default achievements;
