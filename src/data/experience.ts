import type { WorkAchievement, WorkExperience } from '../types/types';

/**
 * Work Experience
 * Contains all professional work history
 * Used on: Experience Page, About Page, Timeline Section
 */

// Achievements for Digital Solutions Strategist
const servirAchievements: WorkAchievement[] = [
    {
        id: 'servier-001',
        metric: 'Customer Segmentation Accuracy',
        improvement: '+35%',
        description: 'Improved accuracy through advanced ML models and feature engineering',
    },
    {
        id: 'servier-002',
        metric: 'User Acquisition',
        improvement: '+40%',
        description: 'Engineered growth experiments with data-driven marketing strategies',
    },
    {
        id: 'servier-003',
        metric: 'Revenue Forecasting',
        improvement: '95% accuracy',
        description: 'Created analytics dashboards enabling real-time product optimization',
    },
    {
        id: 'servier-004',
        metric: 'Infrastructure Efficiency',
        improvement: '-30% costs',
        description: 'Optimized data pipelines reducing infrastructure expenses',
    },
];

// Achievements for Frontend Software Engineer
const tanvirAchievements: WorkAchievement[] = [
    {
        id: 'tanvir-001',
        metric: 'Performance Improvement',
        improvement: '+30%',
        description: 'Through code optimization and best practices',
    },
    {
        id: 'tanvir-002',
        metric: 'Load Time Reduction',
        improvement: '-2.5 seconds',
        description: 'From 5s to 2.5s average page load time',
    },
    {
        id: 'tanvir-003',
        metric: 'User Satisfaction',
        improvement: '+45%',
        description: 'Improved through better UX and performance',
    },
    {
        id: 'tanvir-004',
        metric: 'Development Velocity',
        improvement: '+25%',
        description: 'Through reusable components and design system',
    },
];

/**
 * Work Experience Array
 * Sorted by date (newest first)
 */
export const workExperience: WorkExperience[] = [
    {
        id: 'work-001',
        jobTitle: 'Digital Solutions Strategist',
        company: 'Servier Pharmaceuticals Ltd',
        employmentType: 'Full-time Remote',
        startDate: '2026-01-01',
        endDate: null,
        isCurrent: true,
        location: 'Remote · France',
        duration: '5 months',
        description:
            'Leading data-driven initiatives to optimize customer engagement and drive business growth through intelligent systems and analytics.',
        responsibilities: [
            'Design and implement data pipelines processing 10M+ daily events',
            'Develop ML models for customer segmentation and personalization',
            'Build real-time analytics dashboards for executive decision-making',
            'Lead A/B testing frameworks and growth experiments',
            'Mentor junior developers on best practices in data engineering',
            'Collaborate with product and marketing teams on data-driven strategies',
        ],
        achievements: servirAchievements,
        skills: [
            'Python',
            'Machine Learning',
            'Data Engineering',
            'SQL',
            'Apache Spark',
            'AWS',
            'Docker',
            'Data Visualization',
            'A/B Testing',
            'Business Analytics',
        ],
        companyLogo: '/assets/companies/servier.png',
    },
    {
        id: 'work-002',
        jobTitle: 'Frontend Software Engineer',
        company: 'Tanvir Construction Ltd',
        employmentType: 'Full-time',
        startDate: '2021-06-01',
        endDate: '2023-05-31',
        isCurrent: false,
        location: 'Dhaka, Bangladesh',
        duration: '2 years',
        description: 'Built and maintained customer-facing applications with focus on performance optimization and seamless user experience.',
        responsibilities: [
            'Architected and developed customer-facing web application using Next.js',
            'Implemented responsive UI with Tailwind CSS and modern design patterns',
            'Integrated third-party APIs for real-time data synchronization',
            'Optimized application performance through code splitting and lazy loading',
            'Conducted code reviews and mentored junior developers',
            'Collaborated with backend team for seamless API integration',
        ],
        achievements: tanvirAchievements,
        skills: [
            'React',
            'Next.js',
            'TypeScript',
            'Tailwind CSS',
            'JavaScript',
            'REST APIs',
            'Git',
            'Responsive Design',
            'Web Performance',
            'Component Architecture',
        ],
        companyLogo: '/assets/companies/tanvir.png',
    },
];

/**
 * Get work experience by ID
 */
export const getWorkExperienceById = (id: string): WorkExperience | undefined => {
    return workExperience.find((exp) => exp.id === id);
};

/**
 * Get current work experience
 */
export const getCurrentWork = (): WorkExperience | undefined => {
    return workExperience.find((exp) => exp.isCurrent);
};

/**
 * Get all companies worked for
 */
export const getCompanies = (): string[] => {
    return workExperience.map((exp) => exp.company);
};

/**
 * Calculate total years of experience
 */
export const calculateTotalExperience = (): number => {
    return workExperience.reduce((total, exp) => {
        const start = new Date(exp.startDate).getFullYear();
        const end = exp.endDate ? new Date(exp.endDate).getFullYear() : new Date().getFullYear();
        return total + (end - start);
    }, 0);
};

export default workExperience;
