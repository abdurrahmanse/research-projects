import type { Project } from '../types/types';

/**
 * Projects
 * Contains all portfolio projects
 * Used on: Projects Page, Homepage (featured), About Page
 */

export const projects: Project[] = [
    {
        id: 'proj-001',
        title: 'Healthcare AI Chatbot - Medical Assistance System',
        shortDescription: 'NLP-powered chatbot providing personalized medical guidance and appointment scheduling',
        fullDescription:
            'A sophisticated AI-driven chatbot built to revolutionize patient-healthcare provider communication. The system utilizes advanced NLP techniques to understand patient queries, provide evidence-based medical information, and facilitate seamless appointment scheduling. Integrated with hospital management systems for real-time availability checking.',
        category: 'AI/NLP',
        tags: ['NLP', 'Healthcare', 'AI', 'Python', 'TensorFlow', 'BERT'],
        startDate: '2024-03-01',
        endDate: '2024-09-15',
        status: 'completed',
        featured: true,
        images: ['/assets/projects/healthcare-chatbot-1.png', '/assets/projects/healthcare-chatbot-2.png', '/assets/projects/healthcare-chatbot-3.png'],
        thumbnail: '/assets/projects/healthcare-chatbot-thumb.png',
        technologies: ['Python', 'TensorFlow', 'BERT', 'Flask', 'PostgreSQL', 'Docker', 'AWS'],
        keyFeatures: [
            'Real-time patient query understanding using BERT transformers',
            'Multi-language support (English, Bengali)',
            'Integration with hospital management system',
            'Appointment scheduling and reminders',
            'Patient history tracking and personalization',
            'Doctor recommendation system',
            'Scalable architecture handling 10k+ concurrent users',
        ],
        impact: {
            reduction: '30% reduction in appointment no-shows',
            improvement: '45% improvement in patient satisfaction',
            efficiency: '25% reduction in administrative overhead',
        },
        links: {
            github: 'https://github.com/abdurrahmanse/healthcare-chatbot',
            demo: 'https://healthcare-chatbot-demo.vercel.app',
            documentation: 'https://healthcare-chatbot-docs.vercel.app',
        },
        relatedPublication: 'Transforming Healthcare with AI: Building an NLP-Based Chatbot for Medical Assistance',
    },
    {
        id: 'proj-002',
        title: 'Customer Segmentation Engine',
        shortDescription: 'Transformer-based ML model for advanced customer segmentation and targeting',
        fullDescription:
            'Enterprise-grade machine learning solution utilizing BERT and advanced transformer models to analyze customer behavior patterns and create highly granular customer segments. The system processes millions of transaction records to identify customer personas, predict churn, and enable hyper-personalized marketing strategies.',
        category: 'Machine Learning',
        tags: ['ML', 'Transformers', 'BERT', 'Python', 'Business Analytics'],
        startDate: '2023-06-01',
        endDate: '2024-02-28',
        status: 'completed',
        featured: true,
        images: ['/assets/projects/segmentation-1.png', '/assets/projects/segmentation-2.png'],
        thumbnail: '/assets/projects/segmentation-thumb.png',
        technologies: ['Python', 'PyTorch', 'BERT', 'Scikit-learn', 'Pandas', 'Apache Spark', 'PostgreSQL'],
        keyFeatures: [
            'Advanced feature engineering from raw transactional data',
            'BERT-based behavioral pattern recognition',
            '7-segment customer clustering with business interpretation',
            'Churn prediction with 92% accuracy',
            'Personalization recommendations engine',
            'Real-time segment assignment',
            'Dashboard for segment analysis and performance tracking',
        ],
        impact: {
            accuracy: '87% increase in targeting accuracy',
            revenue: '23% increase in campaign ROI',
            retention: '34% improvement in customer retention',
        },
        links: {
            github: 'https://github.com/abdurrahmanse/customer-segmentation',
            case_study: 'https://abdurrahmans.vercel.app/case-studies/segmentation',
        },
        relatedPublication: 'Leveraging Transformer Models for Enhanced Customer Segmentation',
    },
    {
        id: 'proj-003',
        title: 'Real-time Analytics Dashboard',
        shortDescription: 'Enterprise analytics platform with real-time data visualization and insights',
        fullDescription:
            'A comprehensive analytics platform built with React and modern data visualization libraries. Processes real-time data streams to provide executive dashboards, custom reporting, and predictive insights. Integrates with multiple data sources and provides drill-down capabilities for deep analysis.',
        category: 'Full-stack',
        tags: ['React', 'Data Visualization', 'Real-time', 'Dashboard', 'D3.js'],
        startDate: '2023-12-01',
        endDate: '2024-06-30',
        status: 'completed',
        featured: true,
        images: ['/assets/projects/dashboard-1.png', '/assets/projects/dashboard-2.png', '/assets/projects/dashboard-3.png'],
        thumbnail: '/assets/projects/dashboard-thumb.png',
        technologies: ['React', 'TypeScript', 'D3.js', 'Apache Superset', 'Node.js', 'WebSocket', 'Redis', 'PostgreSQL'],
        keyFeatures: [
            'Real-time data streaming via WebSockets',
            'Interactive visualizations with D3.js',
            'Custom KPI and metric tracking',
            'Drill-down analytics capabilities',
            'Scheduled report generation and distribution',
            'Role-based access control',
            'Mobile-responsive design',
            'Export capabilities (PDF, CSV, Excel)',
        ],
        impact: {
            time: '60% reduction in reporting time',
            insights: '40% faster insight discovery',
            adoption: '95% team adoption rate',
        },
        links: {
            github: 'https://github.com/abdurrahmanse/analytics-dashboard',
            demo: 'https://analytics-dashboard-demo.vercel.app',
        },
    },
    {
        id: 'proj-004',
        title: 'E-commerce Performance Optimization',
        shortDescription: 'Full-stack optimization of e-commerce platform achieving 50% performance improvement',
        fullDescription:
            'Comprehensive performance optimization project for a high-traffic e-commerce platform. Implemented code splitting, lazy loading, server-side rendering, and database optimization resulting in significant improvements in page load time and conversion rates.',
        category: 'Full-stack',
        tags: ['Performance', 'Next.js', 'React', 'Optimization', 'SEO'],
        startDate: '2022-03-01',
        endDate: '2022-11-30',
        status: 'completed',
        featured: false,
        images: ['/assets/projects/ecommerce-1.png'],
        thumbnail: '/assets/projects/ecommerce-thumb.png',
        technologies: ['Next.js', 'React', 'TypeScript', 'Node.js', 'MongoDB', 'Redis', 'CloudFront'],
        keyFeatures: [
            'Code splitting and dynamic imports',
            'Image optimization and lazy loading',
            'Server-side rendering for SEO',
            'Database query optimization',
            'Caching strategies with Redis',
            'CDN integration',
            'Performance monitoring and alerts',
        ],
        impact: {
            speed: '50% reduction in page load time',
            conversion: '28% increase in conversion rate',
            bounce: '35% reduction in bounce rate',
        },
        links: {
            github: 'https://github.com/abdurrahmanse/ecommerce-optimization',
        },
    },
    {
        id: 'proj-005',
        title: 'Predictive Maintenance System',
        shortDescription: 'IoT and ML-based system for predicting equipment failures',
        fullDescription:
            'Advanced machine learning system that analyzes sensor data from industrial equipment to predict failures before they occur. Uses deep learning and statistical analysis to identify patterns and anomalies, enabling proactive maintenance scheduling.',
        category: 'Machine Learning',
        tags: ['Deep Learning', 'IoT', 'Predictive Analytics', 'Time-series'],
        startDate: '2024-04-01',
        endDate: '2024-08-15',
        status: 'completed',
        featured: true,
        images: ['/assets/projects/maintenance-1.png', '/assets/projects/maintenance-2.png'],
        thumbnail: '/assets/projects/maintenance-thumb.png',
        technologies: ['Python', 'TensorFlow', 'LSTM', 'Pandas', 'Apache Kafka', 'InfluxDB', 'AWS IoT Core'],
        keyFeatures: [
            'LSTM-based time-series forecasting',
            'Anomaly detection algorithms',
            'Real-time alert system',
            'Historical trend analysis',
            'Maintenance recommendation engine',
            'Scalable architecture for 1000+ sensors',
            'Integration with existing maintenance systems',
        ],
        impact: {
            downtime: '40% reduction in unplanned downtime',
            maintenance: '35% optimization in maintenance costs',
            efficiency: '25% improvement in equipment efficiency',
        },
        links: {
            github: 'https://github.com/abdurrahmanse/predictive-maintenance',
        },
    },
    {
        id: 'proj-006',
        title: 'Social Media Analytics Platform',
        shortDescription: 'NLP-powered sentiment analysis and social media trend tracking',
        fullDescription:
            'Comprehensive platform for analyzing social media conversations, tracking brand sentiment, and identifying emerging trends. Employs state-of-the-art NLP models for sentiment analysis, topic modeling, and influencer identification.',
        category: 'NLP',
        tags: ['NLP', 'Sentiment Analysis', 'React', 'Python', 'Real-time'],
        startDate: '2023-09-01',
        endDate: '2024-04-30',
        status: 'completed',
        featured: false,
        images: ['/assets/projects/social-analytics-1.png'],
        thumbnail: '/assets/projects/social-analytics-thumb.png',
        technologies: ['Python', 'NLTK', 'TextBlob', 'React', 'Node.js', 'MongoDB', 'Celery'],
        keyFeatures: [
            'Multi-language sentiment analysis',
            'Trend detection and forecasting',
            'Influencer identification',
            'Crisis alert system',
            'Competitive analysis',
            'Real-time monitoring',
            'Custom report generation',
        ],
        impact: {
            insights: '50% faster insight generation',
            sentiment: '88% accuracy in sentiment classification',
            efficiency: '45% reduction in manual analysis time',
        },
        links: {
            github: 'https://github.com/abdurrahmanse/social-analytics',
        },
    },
];

/**
 * Get project by ID
 */
export const getProjectById = (id: string): Project | undefined => {
    return projects.find((proj) => proj.id === id);
};

/**
 * Get featured projects
 */
export const getFeaturedProjects = (): Project[] => {
    return projects.filter((proj) => proj.featured).slice(0, 3);
};

/**
 * Get projects by category
 */
export const getProjectsByCategory = (category: string): Project[] => {
    return projects.filter((proj) => proj.category === category);
};

/**
 * Get projects by technology
 */
export const getProjectsByTechnology = (tech: string): Project[] => {
    return projects.filter((proj) => proj.technologies.includes(tech));
};

/**
 * Get all unique categories
 */
export const getCategories = (): string[] => {
    const categories = new Set<string>();
    projects.forEach((proj) => {
        categories.add(proj.category);
    });
    return Array.from(categories);
};

/**
 * Get all unique technologies
 */
export const getAllTechnologies = (): string[] => {
    const technologies = new Set<string>();
    projects.forEach((proj) => {
        proj.technologies.forEach((tech) => {
            technologies.add(tech);
        });
    });
    return Array.from(technologies);
};

/**
 * Get all unique tags
 */
export const getAllTags = (): string[] => {
    const tags = new Set<string>();
    projects.forEach((proj) => {
        proj.tags.forEach((tag) => {
            tags.add(tag);
        });
    });
    return Array.from(tags);
};

export default projects;
