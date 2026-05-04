/**
 * Statistics & Metrics
 * Contains overall portfolio and career statistics
 * Used on: Homepage (hero section), About Page, Portfolio Overview
 */

export interface Statistic {
    id: string;
    label: string;
    value: string | number;
    description?: string;
    icon?: string;
    trend?: 'up' | 'down' | 'stable';
}

export const statistics: Statistic[] = [
    {
        id: 'stat-001',
        label: 'Years of Experience',
        value: '5+',
        description: 'In full-stack development and AI/ML',
        icon: 'calendar',
    },
    {
        id: 'stat-002',
        label: 'Projects Completed',
        value: 25,
        description: 'Across various industries and technologies',
        icon: 'briefcase',
    },
    {
        id: 'stat-003',
        label: 'Clients Worked With',
        value: 12,
        description: 'Including Fortune 500 companies',
        icon: 'users',
    },
    {
        id: 'stat-004',
        label: 'Research Publications',
        value: 4,
        description: 'In top-tier journals with 82+ citations',
        icon: 'book-open',
    },
    {
        id: 'stat-005',
        label: 'Professional Certifications',
        value: 5,
        description: 'AWS, Google Cloud, TensorFlow, Kubernetes, Docker',
        icon: 'award',
    },
    {
        id: 'stat-006',
        label: 'GitHub Followers',
        value: 1850,
        description: 'Active open-source contributor',
        icon: 'github',
        trend: 'up',
    },
    {
        id: 'stat-007',
        label: 'LinkedIn Connections',
        value: 3420,
        description: 'Professional network',
        icon: 'linkedin',
        trend: 'up',
    },
    {
        id: 'stat-008',
        label: 'Average Project Satisfaction',
        value: '4.9/5',
        description: 'Based on client testimonials',
        icon: 'star',
    },
    {
        id: 'stat-009',
        label: 'Technologies Mastered',
        value: 30,
        description: 'Across frontend, backend, ML, and DevOps',
        icon: 'code',
    },
    {
        id: 'stat-010',
        label: 'Open Source Contributions',
        value: 150,
        description: 'Pull requests to various projects',
        icon: 'git-branch',
    },
];

/**
 * Get statistic by ID
 */
export const getStatisticById = (id: string): Statistic | undefined => {
    return statistics.find((stat) => stat.id === id);
};

/**
 * Get statistics by category (experience, projects, learning, etc.)
 */
export const getCareerStatistics = (): Statistic[] => {
    return statistics.filter((stat) =>
        ['stat-001', 'stat-002', 'stat-003', 'stat-005'].includes(stat.id),
    );
};

/**
 * Get social statistics
 */
export const getSocialStatistics = (): Statistic[] => {
    return statistics.filter((stat) => ['stat-006', 'stat-007'].includes(stat.id));
};

/**
 * Get achievement statistics
 */
export const getAchievementStatistics = (): Statistic[] => {
    return statistics.filter((stat) =>
        ['stat-004', 'stat-008', 'stat-009', 'stat-010'].includes(stat.id),
    );
};

/**
 * Get all statistics
 */
export const getAllStatistics = (): Statistic[] => {
    return statistics;
};

/**
 * Get statistics with trends
 */
export const getStatisticsWithTrends = (): Statistic[] => {
    return statistics.filter((stat) => stat.trend !== undefined);
};

export default statistics;
