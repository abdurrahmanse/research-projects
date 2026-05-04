import type { Education } from '../types/types';

/**
 * Education
 * Contains all educational background
 * Used on: About Page, Education Section, Timeline
 */

export const education: Education[] = [
    {
        id: 'edu-001',
        degree: 'M.Sc. in Computer Science & Engineering',
        institution: 'Dhaka University of Engineering & Technology',
        startDate: '2025-01-01',
        endDate: '2027-12-31',
        status: 'pursuing',
        gpa: '3.8/4.0',
        location: 'Dhaka, Bangladesh',
        description:
            'Advanced studies in AI/ML, Deep Learning, NLP, and Computer Vision with focus on Transformer models, BERT, and GANs. Involved in cutting-edge research and development of machine learning models that power production systems and business decisions.',
        keyCourseworks: [
            'Advanced Machine Learning',
            'Natural Language Processing',
            'Computer Vision',
            'Deep Learning',
            'Transformer Models & BERT',
            'Generative Adversarial Networks',
            'Reinforcement Learning',
            'MLOps & Model Deployment',
        ],
        highlights: ['Published 2 research papers', 'Working on novel NLP applications', 'Building production ML systems'],
    },
    {
        id: 'edu-002',
        degree: 'B.Sc. in Computer Science & Engineering',
        institution: 'Green University of Bangladesh',
        startDate: '2020-01-01',
        endDate: '2024-12-31',
        status: 'completed',
        gpa: '3.75/4.0',
        location: 'Dhaka, Bangladesh',
        description:
            'Strong foundation in Software Development, Algorithm Design, and Hardware-Software Integration. Built expertise in high-demand, high-paying tech skills with focus on practical application and real-world problem solving.',
        keyCourseworks: [
            'Data Structures & Algorithms',
            'Database Management Systems',
            'Web Development',
            'Software Engineering',
            'Artificial Intelligence',
            'Computer Networks',
            'Operating Systems',
            'System Design',
        ],
        highlights: ['Dean\'s List (2022, 2023)', 'Best Student Award - Web Development (2019)', 'Led multiple academic projects'],
    },
];

/**
 * Get education by ID
 */
export const getEducationById = (id: string): Education | undefined => {
    return education.find((edu) => edu.id === id);
};

/**
 * Get completed education
 */
export const getCompletedEducation = (): Education[] => {
    return education.filter((edu) => edu.status === 'completed');
};

/**
 * Get ongoing education
 */
export const getOngoingEducation = (): Education[] => {
    return education.filter((edu) => edu.status === 'pursuing');
};

/**
 * Get highest degree
 */
export const getHighestDegree = (): Education | undefined => {
    return education.length > 0 ? education[0] : undefined;
};

/**
 * Get all unique courseworks across all education
 */
export const getAllCourseworks = (): string[] => {
    const allCourseworks: string[] = [];
    education.forEach((edu) => {
        allCourseworks.push(...edu.keyCourseworks);
    });
    return [...new Set(allCourseworks)];
};

export default education;
