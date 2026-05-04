import type { Publication } from '../types/types';

/**
 * Publications
 * Contains all research papers and publications
 * Used on: Research Page, About Page, Resume
 */

export const publications: Publication[] = [
    {
        id: 'pub-001',
        title: 'Transforming Healthcare with AI: Building an NLP-Based Chatbot for Medical Assistance',
        authors: ['Abdur Rahman'],
        journal: 'Journal of AI and Healthcare',
        publishedDate: '2024-06-15',
        volume: '2',
        issue: '3',
        pages: '145-162',
        doi: '10.1234/jah.2024.001',
        abstract:
            'This paper explores the integration of natural language processing in the healthcare sector to improve patient communication and service efficiency. We present a novel approach using BERT and transformer-based models to build an intelligent chatbot system that understands complex medical queries and provides evidence-based guidance. Our system demonstrates 92% accuracy in query classification and 45% improvement in patient satisfaction scores.',
        keywords: ['NLP', 'Healthcare', 'BERT', 'Chatbot', 'Deep Learning'],
        type: 'journal',
        status: 'published',
        links: {
            paper: 'https://example.com/papers/healthcare-ai-chatbot.pdf',
            doi: 'https://doi.org/10.1234/jah.2024.001',
            github: 'https://github.com/abdurrahmanse/healthcare-chatbot',
        },
        citations: 23,
        downloads: 1245,
        researchArea: 'Natural Language Processing & Healthcare AI',
    },
    {
        id: 'pub-002',
        title: 'Leveraging Transformer Models for Enhanced Customer Segmentation',
        authors: ['Abdur Rahman'],
        journal: 'Journal of Data Science and Marketing',
        publishedDate: '2023-09-20',
        volume: '1',
        issue: '2',
        pages: '78-95',
        doi: '10.1234/jdsm.2023.002',
        abstract:
            'This article discusses the application of BERT and other transformer models to refine customer segmentation, leading to more targeted marketing strategies. We propose a comprehensive framework for behavioral analysis using pre-trained transformer models, achieving 87% improvement in segmentation accuracy compared to traditional methods. The study includes case studies from three major e-commerce companies demonstrating practical applicability.',
        keywords: ['Transformers', 'BERT', 'Customer Segmentation', 'Machine Learning', 'Marketing'],
        type: 'journal',
        status: 'published',
        links: {
            paper: 'https://example.com/papers/customer-segmentation.pdf',
            doi: 'https://doi.org/10.1234/jdsm.2023.002',
            github: 'https://github.com/abdurrahmanse/customer-segmentation',
        },
        citations: 34,
        downloads: 1890,
        researchArea: 'Machine Learning & Business Analytics',
    },
    {
        id: 'pub-003',
        title: 'Deep Learning Approaches for Real-time Anomaly Detection in IoT Systems',
        authors: ['Abdur Rahman', 'Dr. Ahmed Hassan'],
        journal: 'International Journal of IoT and Embedded Systems',
        publishedDate: '2024-03-10',
        volume: '5',
        issue: '1',
        pages: '34-52',
        doi: '10.1234/ijes.2024.003',
        abstract:
            'This paper presents novel deep learning architectures for detecting anomalies in IoT sensor data streams. We propose an LSTM-based approach combined with autoencoder techniques to identify unusual patterns with 94% precision. The system handles real-time data from multiple sources and provides low-latency alerts for critical anomalies.',
        keywords: ['Deep Learning', 'IoT', 'Anomaly Detection', 'LSTM', 'Real-time Processing'],
        type: 'journal',
        status: 'published',
        links: {
            paper: 'https://example.com/papers/iot-anomaly-detection.pdf',
            doi: 'https://doi.org/10.1234/ijes.2024.003',
        },
        citations: 15,
        downloads: 845,
        researchArea: 'Deep Learning & IoT Systems',
    },
    {
        id: 'pub-004',
        title: 'Efficient Full-Stack Web Development with React and Node.js: A Practical Guide',
        authors: ['Abdur Rahman'],
        journal: 'International Journal of Web Engineering',
        publishedDate: '2023-06-15',
        volume: '8',
        issue: '2',
        pages: '112-128',
        doi: '10.1234/ijwe.2023.004',
        abstract:
            'A comprehensive guide to building scalable web applications using React and Node.js. The paper covers best practices for architecture design, performance optimization, and deployment strategies. Includes detailed case study of an e-commerce platform achieving 50% performance improvement.',
        keywords: ['React', 'Node.js', 'Web Development', 'Performance Optimization', 'Scalability'],
        type: 'journal',
        status: 'published',
        links: {
            paper: 'https://example.com/papers/fullstack-development.pdf',
            doi: 'https://doi.org/10.1234/ijwe.2023.004',
        },
        citations: 12,
        downloads: 567,
        researchArea: 'Full-Stack Web Development',
    },
];

/**
 * Get publication by ID
 */
export const getPublicationById = (id: string): Publication | undefined => {
    return publications.find((pub) => pub.id === id);
};

/**
 * Get publications by author
 */
export const getPublicationsByAuthor = (author: string): Publication[] => {
    return publications.filter((pub) => pub.authors.includes(author));
};

/**
 * Get publications by research area
 */
export const getPublicationsByResearchArea = (area: string): Publication[] => {
    return publications.filter((pub) => pub.researchArea === area);
};

/**
 * Get total citations
 */
export const getTotalCitations = (): number => {
    return publications.reduce((total, pub) => total + pub.citations, 0);
};

/**
 * Get total downloads
 */
export const getTotalDownloads = (): number => {
    return publications.reduce((total, pub) => total + pub.downloads, 0);
};

/**
 * Get most cited publication
 */
export const getMostCitedPublication = (): Publication | undefined => {
    return publications.reduce((prev, current) => (prev.citations > current.citations ? prev : current));
};

/**
 * Get most downloaded publication
 */
export const getMostDownloadedPublication = (): Publication | undefined => {
    return publications.reduce((prev, current) => (prev.downloads > current.downloads ? prev : current));
};

/**
 * Get all research areas
 */
export const getResearchAreas = (): string[] => {
    const areas = new Set<string>();
    publications.forEach((pub) => {
        areas.add(pub.researchArea);
    });
    return Array.from(areas);
};

/**
 * Get all keywords
 */
export const getAllKeywords = (): string[] => {
    const keywords = new Set<string>();
    publications.forEach((pub) => {
        pub.keywords.forEach((keyword) => {
            keywords.add(keyword);
        });
    });
    return Array.from(keywords);
};

export default publications;
