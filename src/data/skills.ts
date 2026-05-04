import type { SkillCategory, SoftSkill } from '../types/types';

/**
 * Technical Skills
 * Contains all technical skills organized by category
 * Used on: Skills Page, About Page, Experience Page
 */

export const technicalSkills: SkillCategory[] = [
    {
        category: 'Programming Languages',
        skills: [
            {
                name: 'Python',
                proficiency: 'Expert',
                years: 3,
                endorsements: 145,
                description: 'Advanced Python programming for data science, ML, and backend development',
            },
            {
                name: 'TypeScript',
                proficiency: 'Expert',
                years: 4,
                endorsements: 156,
                description: 'Strong typing for large-scale JavaScript applications',
            },
            {
                name: 'JavaScript',
                proficiency: 'Expert',
                years: 5,
                endorsements: 189,
                description: 'Full proficiency in modern JavaScript ES6+ and async programming',
            },
            {
                name: 'SQL',
                proficiency: 'Advanced',
                years: 3,
                endorsements: 98,
                description: 'Complex queries, optimization, and database design',
            },
        ],
    },
    {
        category: 'Frontend Technologies',
        skills: [
            {
                name: 'React',
                proficiency: 'Expert',
                years: 4,
                endorsements: 167,
                description: 'Component design, state management, hooks, and optimization',
            },
            {
                name: 'Next.js',
                proficiency: 'Advanced',
                years: 3,
                endorsements: 134,
                description: 'SSR, SSG, API routes, and production deployment',
            },
            {
                name: 'Tailwind CSS',
                proficiency: 'Expert',
                years: 3,
                endorsements: 112,
                description: 'Utility-first CSS for rapid UI development',
            },
            {
                name: 'HTML5 & CSS3',
                proficiency: 'Expert',
                years: 5,
                endorsements: 156,
                description: 'Semantic HTML and advanced CSS techniques',
            },
        ],
    },
    {
        category: 'Backend Technologies',
        skills: [
            {
                name: 'Node.js',
                proficiency: 'Advanced',
                years: 3,
                endorsements: 123,
                description: 'Server-side JavaScript, REST APIs, and real-time applications',
            },
            {
                name: 'Express.js',
                proficiency: 'Advanced',
                years: 3,
                endorsements: 98,
                description: 'Middleware, routing, and API development',
            },
            {
                name: 'MongoDB',
                proficiency: 'Advanced',
                years: 2,
                endorsements: 87,
                description: 'NoSQL database design and optimization',
            },
            {
                name: 'PostgreSQL',
                proficiency: 'Advanced',
                years: 3,
                endorsements: 105,
                description: 'Relational database design, migrations, and optimization',
            },
        ],
    },
    {
        category: 'Data Science & ML',
        skills: [
            {
                name: 'Machine Learning',
                proficiency: 'Expert',
                years: 3,
                endorsements: 156,
                description: 'Supervised/unsupervised learning, model selection, and evaluation',
            },
            {
                name: 'Deep Learning',
                proficiency: 'Advanced',
                years: 2,
                endorsements: 134,
                description: 'Neural networks, CNN, RNN, and optimization techniques',
            },
            {
                name: 'Natural Language Processing',
                proficiency: 'Advanced',
                years: 2,
                endorsements: 128,
                description: 'Text processing, NLP models, and transformer architectures',
            },
            {
                name: 'Computer Vision',
                proficiency: 'Advanced',
                years: 2,
                endorsements: 112,
                description: 'Image processing, CNN models, and object detection',
            },
            {
                name: 'Data Analysis',
                proficiency: 'Expert',
                years: 3,
                endorsements: 145,
                description: 'Statistical analysis, data visualization, and insights extraction',
            },
        ],
    },
    {
        category: 'Cloud & DevOps',
        skills: [
            {
                name: 'AWS',
                proficiency: 'Advanced',
                years: 2,
                endorsements: 98,
                description: 'EC2, S3, Lambda, RDS, and SageMaker',
            },
            {
                name: 'Docker',
                proficiency: 'Advanced',
                years: 2,
                endorsements: 87,
                description: 'Containerization and orchestration',
            },
            {
                name: 'Git & GitHub',
                proficiency: 'Expert',
                years: 5,
                endorsements: 178,
                description: 'Version control, branching strategies, and CI/CD',
            },
        ],
    },
    {
        category: 'Tools & Frameworks',
        skills: [
            {
                name: 'TensorFlow',
                proficiency: 'Advanced',
                years: 2,
                endorsements: 98,
                description: 'Deep learning framework for production models',
            },
            {
                name: 'PyTorch',
                proficiency: 'Advanced',
                years: 2,
                endorsements: 102,
                description: 'PyTorch for research and production ML models',
            },
            {
                name: 'Scikit-learn',
                proficiency: 'Expert',
                years: 2,
                endorsements: 156,
                description: 'Classical machine learning algorithms and utilities',
            },
            {
                name: 'Pandas & NumPy',
                proficiency: 'Expert',
                years: 3,
                endorsements: 167,
                description: 'Data manipulation and numerical computing',
            },
            {
                name: 'Jupyter & IPython',
                proficiency: 'Advanced',
                years: 3,
                endorsements: 123,
                description: 'Interactive data analysis and visualization',
            },
        ],
    },
];

/**
 * Soft Skills
 * Contains all soft/interpersonal skills
 */
export const softSkills: SoftSkill[] = [
    {
        name: 'Leadership',
        proficiency: 'Advanced',
        endorsements: 67,
        description: 'Team leadership, mentoring, and project management',
    },
    {
        name: 'Communication',
        proficiency: 'Advanced',
        endorsements: 89,
        description: 'Clear technical communication and documentation',
    },
    {
        name: 'Problem-Solving',
        proficiency: 'Expert',
        endorsements: 156,
        description: 'Complex problem analysis and solution design',
    },
    {
        name: 'Project Management',
        proficiency: 'Advanced',
        endorsements: 76,
        description: 'Agile, Scrum, and cross-functional collaboration',
    },
    {
        name: 'Data-Driven Decision Making',
        proficiency: 'Expert',
        endorsements: 134,
        description: 'Analytics-based strategy and optimization',
    },
];

/**
 * Get all technical skills as flat array
 */
export const getAllTechnicalSkills = (): string[] => {
    const skills: string[] = [];
    technicalSkills.forEach((category) => {
        category.skills.forEach((skill) => {
            skills.push(skill.name);
        });
    });
    return skills;
};

/**
 * Get skills by category
 */
export const getSkillsByCategory = (category: string): string[] => {
    const categoryData = technicalSkills.find((cat) => cat.category === category);
    return categoryData ? categoryData.skills.map((skill) => skill.name) : [];
};

/**
 * Get expert-level skills
 */
export const getExpertSkills = (): string[] => {
    const skills: string[] = [];
    technicalSkills.forEach((category) => {
        category.skills.forEach((skill) => {
            if (skill.proficiency === 'Expert') {
                skills.push(skill.name);
            }
        });
    });
    softSkills.forEach((skill) => {
        if (skill.proficiency === 'Expert') {
            skills.push(skill.name);
        }
    });
    return skills;
};

/**
 * Get skills by proficiency level
 */
export const getSkillsByProficiency = (proficiency: 'Beginner' | 'Intermediate' | 'Advanced' | 'Expert'): string[] => {
    const skills: string[] = [];
    technicalSkills.forEach((category) => {
        category.skills.forEach((skill) => {
            if (skill.proficiency === proficiency) {
                skills.push(skill.name);
            }
        });
    });
    return skills;
};

/**
 * Get total endorsements across all skills
 */
export const getTotalEndorsements = (): number => {
    let total = 0;
    technicalSkills.forEach((category) => {
        category.skills.forEach((skill) => {
            total += skill.endorsements;
        });
    });
    softSkills.forEach((skill) => {
        total += skill.endorsements;
    });
    return total;
};

export default { technicalSkills, softSkills };
