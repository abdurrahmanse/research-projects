import type { Service } from '../types/types';

/**
 * Services
 * Contains all service offerings
 * Used on: Services Page, Homepage
 */

export const services: Service[] = [
    {
        id: 'service-001',
        name: 'Machine Learning Solutions',
        shortDescription: 'Custom ML models and AI solutions tailored to your business needs.',
        fullDescription:
            'End-to-end machine learning solutions from problem definition to model deployment. Includes data preparation, feature engineering, model selection, training, evaluation, and production deployment.',
        category: 'Artificial Intelligence',
        icon: 'brain-circuit',
        price: 'Custom',
        deliverables: [
            'Requirements analysis and problem definition',
            'Data collection and preparation',
            'Model development and training',
            'Performance evaluation and optimization',
            'Production deployment and monitoring',
            'Team training and documentation',
        ],
        technologies: ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'AWS SageMaker'],
        timeline: '4-12 weeks',
        featured: true,
    },
    {
        id: 'service-002',
        name: 'Data Engineering & Pipelines',
        shortDescription: 'Build scalable data infrastructure and pipelines.',
        fullDescription:
            'Design and implement robust data pipelines that handle massive volumes of data reliably. Includes data collection, transformation, storage, and analytics infrastructure.',
        category: 'Data Engineering',
        icon: 'database',
        price: 'Custom',
        deliverables: [
            'Data architecture design',
            'ETL/ELT pipeline development',
            'Data warehouse setup',
            'Real-time streaming pipelines',
            'Data quality monitoring',
            'Documentation and training',
        ],
        technologies: ['Apache Spark', 'Apache Kafka', 'PostgreSQL', 'MongoDB', 'AWS'],
        timeline: '6-16 weeks',
        featured: true,
    },
    {
        id: 'service-003',
        name: 'Full-Stack Web Development',
        shortDescription: 'Modern, scalable web applications from frontend to backend.',
        fullDescription:
            'Complete web application development using latest technologies and best practices. Includes design, development, testing, deployment, and maintenance.',
        category: 'Web Development',
        icon: 'code',
        price: 'Custom',
        deliverables: [
            'Frontend development (React, Next.js)',
            'Backend development (Node.js, Python)',
            'Database design and optimization',
            'API development and documentation',
            'Testing and quality assurance',
            'Deployment and DevOps setup',
        ],
        technologies: ['React', 'Next.js', 'Node.js', 'TypeScript', 'PostgreSQL', 'Docker'],
        timeline: '8-20 weeks',
        featured: true,
    },
    {
        id: 'service-004',
        name: 'Performance Optimization',
        shortDescription: 'Speed up your applications and systems.',
        fullDescription:
            'Comprehensive performance optimization for web applications, databases, and infrastructure. Identify bottlenecks and implement solutions for significant improvements.',
        category: 'Optimization',
        icon: 'zap',
        price: 'Custom',
        deliverables: [
            'Performance audit and analysis',
            'Bottleneck identification',
            'Code optimization',
            'Database optimization',
            'Caching strategies',
            'Performance monitoring setup',
        ],
        technologies: ['Next.js', 'React', 'Node.js', 'PostgreSQL', 'Redis'],
        timeline: '2-6 weeks',
        featured: false,
    },
    {
        id: 'service-005',
        name: 'NLP & Text Analysis',
        shortDescription: 'Advanced natural language processing solutions.',
        fullDescription:
            'Leverage cutting-edge NLP techniques for sentiment analysis, classification, chatbots, and more. Custom solutions for your specific text analysis needs.',
        category: 'NLP',
        icon: 'message-circle',
        price: 'Custom',
        deliverables: [
            'Problem definition and feasibility analysis',
            'Model selection and development',
            'Fine-tuning and optimization',
            'Integration with existing systems',
            'API development',
            'Documentation and support',
        ],
        technologies: ['Python', 'BERT', 'TensorFlow', 'NLTK', 'Hugging Face'],
        timeline: '4-10 weeks',
        featured: false,
    },
    {
        id: 'service-006',
        name: 'AI/ML Consulting',
        shortDescription: 'Strategic consulting for AI and ML initiatives.',
        fullDescription:
            'Expert guidance on AI strategy, technology selection, team building, and implementation. Help your organization leverage AI effectively.',
        category: 'Consulting',
        icon: 'lightbulb',
        price: 'Custom',
        deliverables: [
            'AI strategy development',
            'Technology assessment and recommendation',
            'Team building and training',
            'Implementation roadmap',
            'Risk mitigation planning',
            'Ongoing advisory support',
        ],
        technologies: ['Various'],
        timeline: '4-12 weeks',
        featured: false,
    },
];

/**
 * Get service by ID
 */
export const getServiceById = (id: string): Service | undefined => {
    return services.find((service) => service.id === id);
};

/**
 * Get featured services
 */
export const getFeaturedServices = (): Service[] => {
    return services.filter((service) => service.featured);
};

/**
 * Get services by category
 */
export const getServicesByCategory = (category: string): Service[] => {
    return services.filter((service) => service.category === category);
};

/**
 * Get services by technology
 */
export const getServicesByTechnology = (tech: string): Service[] => {
    return services.filter((service) => service.technologies.includes(tech));
};

/**
 * Get all unique categories
 */
export const getCategories = (): string[] => {
    const categories = new Set<string>();
    services.forEach((service) => {
        categories.add(service.category);
    });
    return Array.from(categories);
};

/**
 * Get all unique technologies used
 */
export const getAllTechnologies = (): string[] => {
    const technologies = new Set<string>();
    services.forEach((service) => {
        service.technologies.forEach((tech) => {
            technologies.add(tech);
        });
    });
    return Array.from(technologies);
};

/**
 * Search services by name or description
 */
export const searchServices = (query: string): Service[] => {
    const lowerQuery = query.toLowerCase();
    return services.filter(
        (service) =>
            service.name.toLowerCase().includes(lowerQuery) ||
            service.shortDescription.toLowerCase().includes(lowerQuery) ||
            service.fullDescription.toLowerCase().includes(lowerQuery),
    );
};

export default services;
